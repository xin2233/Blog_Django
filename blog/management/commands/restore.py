"""从备份文件恢复博客数据：全量数据 + 媒体文件。

数据库无关：通过 loaddata 导入数据，兼容 SQLite / MySQL / PostgreSQL 等。
"""
import os
import tarfile
import tempfile
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = '从 .tar.gz 备份文件恢复博客数据，支持多数据库'

    def add_arguments(self, parser):
        parser.add_argument('backup_file', help='备份文件路径 (.tar.gz)')

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        if not os.path.exists(backup_file):
            raise CommandError(f'备份文件不存在: {backup_file}')

        if not tarfile.is_tarfile(backup_file):
            raise CommandError('文件不是有效的 tar.gz 格式')

        media_root = settings.MEDIA_ROOT

        # 询问确认
        self.stdout.write(self.style.WARNING(
            '警告：恢复将覆盖当前数据库和媒体文件！\n'
            f'  数据库: {settings.DATABASES["default"]["ENGINE"]}\n'
            f'  媒体文件: {media_root}\n'
        ))
        confirm = input('确认继续? (yes/no): ')
        if confirm.lower() not in ('yes', 'y'):
            self.stdout.write('已取消。')
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            # 解压备份到临时目录
            self.stdout.write('正在解压备份文件...')
            with tarfile.open(backup_file, 'r:gz') as tar:
                tar.extractall(path=tmpdir)

            # 恢复数据（使用 loaddata）
            data_json = os.path.join(tmpdir, 'data.json')
            if not os.path.exists(data_json):
                raise CommandError('备份文件中缺少 data.json，请确认备份文件完整。')

            self.stdout.write('正在导入数据（可能会覆盖现有数据）...')
            # 先清空现有数据（通过 flush 重置自增 ID）
            self.stdout.write('  清空现有数据...')
            call_command('flush', '--noinput', verbosity=0)
            self.stdout.write('  加载备份数据...')
            call_command('loaddata', data_json, verbosity=1)
            self.stdout.write(self.style.SUCCESS('  数据导入完成。'))

            # 恢复媒体文件
            media_tmp = os.path.join(tmpdir, 'media')
            if os.path.exists(media_tmp):
                if os.path.exists(media_root):
                    shutil.rmtree(media_root)
                shutil.copytree(media_tmp, media_root, symlinks=True)
                self.stdout.write('媒体文件已恢复。')
            else:
                self.stdout.write(self.style.WARNING('备份文件中没有 media 目录，跳过。'))

        self.stdout.write(self.style.SUCCESS(f'恢复成功: {backup_file}'))
        self.stdout.write(self.style.WARNING('请重启 Django 服务以确保生效。'))