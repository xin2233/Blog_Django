"""备份博客数据：全量数据 + 媒体文件 → .tar.gz 文件。

数据库无关：通过 dumpdata 导出数据，兼容 SQLite / MySQL / PostgreSQL 等。
"""
import os
import tarfile
import tempfile
import shutil
from datetime import datetime
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '备份博客数据（全量数据 + 媒体文件）到 .tar.gz 文件，支持多数据库'

    def add_arguments(self, parser):
        parser.add_argument('output', nargs='?', default=None,
                            help='备份文件路径（默认: backups/blog-<日期>.tar.gz）')

    def handle(self, *args, **options):
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        output = options['output']
        if not output:
            stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output = os.path.join(backup_dir, f'blog_backup_{stamp}.tar.gz')

        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. dumpdata 导出全量数据到 JSON
            self.stdout.write('正在导出数据...')
            buf = StringIO()
            call_command(
                'dumpdata',
                '--exclude', 'contenttypes',
                '--exclude', 'auth.permission',
                '--exclude', 'sessions',
                '--format', 'json',
                '--indent', '2',
                stdout=buf,
            )
            data_json = buf.getvalue()
            json_path = os.path.join(tmpdir, 'data.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                f.write(data_json)
            self.stdout.write(self.style.SUCCESS(f'  数据导出完成 ({len(data_json) / 1024:.1f} KB)'))

            # 2. 复制 media 目录
            media_tmp = os.path.join(tmpdir, 'media')
            if os.path.exists(settings.MEDIA_ROOT):
                shutil.copytree(settings.MEDIA_ROOT, media_tmp, symlinks=True)
                self.stdout.write(f'  媒体文件已打包 ({len(os.listdir(media_tmp))} 个文件/目录)')

            # 3. 打包为 .tar.gz
            with tarfile.open(output, 'w:gz') as tar:
                tar.add(json_path, arcname='data.json')
                if os.path.exists(media_tmp):
                    tar.add(media_tmp, arcname='media')

        size = os.path.getsize(output)
        self.stdout.write(self.style.SUCCESS(
            f'备份成功: {output} ({size / 1024:.1f} KB)'
        ))