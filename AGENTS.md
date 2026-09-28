# Blog_Django — Agent Guide

## Project Overview
Django 5.2 blog with Python 3.12. Two apps: `blog` (posts, categories, tags, comments, sidebar) and `users` (auth). Frontend uses Bulma; backend uses AdminLTE 4 with Bootstrap 5.3.

## Commands
```bash
# 虚拟环境（venv/ 与 .venv/ 都在仓库里且都被 gitignore，先确认哪个装了依赖）
source venv/bin/activate        # README 用的
source .venv/bin/activate       # docs 用的

# Install
pip install -r requirements.txt
# 国内镜像（pip 报 SSL 证书错误时）
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# Database（blog 和 users 都有模型，两个都要生成迁移）
python manage.py makemigrations blog
python manage.py makemigrations users
python manage.py migrate

# Run
python manage.py runserver 0.0.0.0:8080

# Superuser
python manage.py createsuperuser

# 备份 / 恢复（blog/management/commands/）
python manage.py backup                        # → backups/blog_backup_<时间戳>.tar.gz
python manage.py backup /path/to/x.tar.gz
python manage.py restore /path/to/x.tar.gz     # 交互式确认；flush + loaddata，失败整体回滚

# Tests（覆盖草稿过滤、评论审核、备份/恢复命令、登录与密码重置）
python manage.py test                          # 全量
python manage.py test users                    # 按 app 跑
python manage.py test blog.tests.PostVisibilityTests.test_draft_detail_returns_404  # 单条
```

No build tool, linter, or formatter is configured. No `pyproject.toml`.

## Directory Layout
```
MyBlog/           # Django project config (settings.py, urls, wsgi, asgi)
blog/             # Main blog app
  views.py            # Frontend views (index, category_list, post_detail, search, archives, submit_comment)
  views_backend.py    # Custom backend views — all @login_required (article CRUD, category/tag AJAX, backup)
  models.py           # Category, Tag, Post, Comment, Sidebar
  admin.py            # Custom PostAdmin (self-hosted CKEditor5) + CommentAdmin (moderation actions)
  management/commands/backup.py, restore.py    # dumpdata/loaddata + media → .tar.gz
  templatetags/category.py   # get_category_list, get_sidebar_list, get_new_post, get_hot_post,
                             # get_hot_pv_post, get_archives, get_tag_list
users/            # User auth app
  views.py            # login, register, active_user, forget_pwd/forget_pwd_url, profile
  models.py           # UserProfile (OneToOne → User), EmailVerifyRecord
  forms.py            # LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
utils/            # Not an app: email_send.py — 注册激活 / 密码重置邮件与验证码
templates/        # Three template families:
  blog/base.html          # Frontend (Bulma); blog/index.html is reused by search
  blog/backend/           # Custom backend (AdminLTE 4, via backend_base.html)
  blog/sidebar/*.html     # Widget partials rendered by Sidebar.get_content
  users/base.html         # Users (plain, no CSS framework active)
static/           # Assets: bulma, ckeditor5, kindeditor, flatui, bootstrap-3.3.7
backups/          # Gitignored — .tar.gz produced by manage.py backup / the backend web page
media/            # Gitignored — absent in a fresh clone, created on first upload
docs/             # Chinese docs — startup guide, changelog, backlog
temp/             # Gitignored — transient files (AdminLTE v4 zip)
```

## Architecture

- **Auth is not Django-standard.** `MyBackend` in `users/views.py` allows logging in with username *or* email. It is instantiated directly inside `login_view`, **not** registered in `AUTHENTICATION_BACKENDS`, so `django.contrib.auth.authenticate()` never reaches it — don't assume switching that setting affects login. Registration sets `username = email`; activation only flips `is_staff`, and accounts start `is_active=True`, so activation is effectively cosmetic.
- **Email verification chain.** `register` / `forget_pwd` → `utils.email_send.send_register_email()` → row in `EmailVerifyRecord` → `/users/active/<code>` or `/users/forget_pwd_url/<code>`. Codes never expire today. The links are hardcoded to `http://127.0.0.1:8000` in `utils/email_send.py`, so they break under `runserver 0.0.0.0:8080`.
- **Draft/published is filtered in the view layer, not the model layer.** Every public view filters `status='published'`, including the prev/next post lookups; the custom backend reads `Post.objects...` unfiltered. New queries must filter explicitly or drafts leak.
- **Comments are moderated and nested.** `Comment.is_approved` defaults to `False`; only approved, top-level (`parent__isnull=True`) comments render. Replies hang off a self-FK `parent`.
- **Sidebar is data-driven.** `Sidebar.get_content` renders `blog/sidebar/*.html` by `display_type`; templates get their data from the `category.py` template tags, so renaming those tags breaks `base.html`.
- **Two independent admin surfaces** share the same models: `/admin/` (Django admin, `blog/admin.py`) and `/home_backend/` (custom AdminLTE backend, `blog/views_backend.py`). Changing one does not change the other.
- **Static/media serving is DEBUG-only.** `MyBlog/urls.py` appends `static()` for both, but `STATIC_ROOT` is undefined and `static()` returns `[]` when `DEBUG=False` — both silently stop being served in production.

## Non-Obvious Gotchas

1. **`tags` is a ForeignKey, not ManyToManyField** — each Post has exactly one Tag. A ManyToMany refactor would be a breaking change.

2. **Three separate base templates** — `blog/base.html` (Bulma frontend), `blog/backend/backend_base.html` (AdminLTE 4 backend), `users/base.html` (no CSS framework). Do NOT assume one shared base template.

3. **Migrations are now tracked** — `.gitignore` used to ignore `migrations/`; after adding a model, run `makemigrations blog` / `makemigrations users` and commit the result, otherwise a fresh clone has no tables.

4. **`Sidebar` uses `display_type` (int, not a FK)** — switch on `display_type` (1=search, 2=new post, 3=hot post, 4=recent comments, 5=archives, 6=HTML) to render different sidebar widgets. See `Sidebar.get_content` in models.py.

5. **Rich text editors** — Django admin uses self-hosted CKEditor5 assets declared in `blog/admin.py` (`Media`); the custom backend uses KindEditor. Upload endpoints are `/upload_img/` (file field `custom-field-name`) and `/kindeditor_upload_img/` (field `imgFile`), both writing to `media/upload/img/`. The `ckeditor_uploader` route was removed because that app is not in `INSTALLED_APPS`.

6. **URL namespaces** — `blog:index`, `blog:post_detail`, `users:login`, etc. Always use `{% url 'blog:...' %}` or `{% url 'users:...' %}` in templates.

7. **`Paginator` requires ordered QuerySets** — passing unordered data triggers `UnorderedObjectListWarning`. Always chain `.order_by(...)` before paginating. Page size is hardcoded (2 per page on the frontend, 15 in the backend).

8. **Email in DEBUG mode** — uses `django.core.mail.backends.console.EmailBackend` (writes to console). Production: set `EMAIL_HOST`/`EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD` env vars.

9. **`db.sqlite3` is gitignored** — the file exists on disk but won't commit. MySQL config is commented out in settings.py.

10. **Dead files were removed** — `blog/forms.py` (incomplete `EmpForm`) and `utils/upload.py` have been deleted; don't assume they exist, and don't add files without callers.

11. **`media/` may not exist** — it is gitignored and absent in a fresh clone. The upload views create `media/upload/img/` on demand; any new code writing under `MEDIA_ROOT` must `os.makedirs(..., exist_ok=True)` first.

12. **`restore` is destructive** — it runs `flush` + `loaddata` in one transaction and deletes `MEDIA_ROOT` before restoring media. Both extractions use `tar.extractall(..., filter='data')` (path-traversal fix); keep that argument.

13. **Two virtualenvs** (`venv/`, `.venv/`) exist in the tree, both gitignored. Check which one has the packages installed before running manage.py.

14. **The roadmap lives in `docs/待办功能清单.md`** — it flags the `tags` → M2M change as breaking and proposes a `blog/services.py` service layer. Check it before refactoring.

15. **`README.md` and `docs/` are Chinese** — keep new docs in Chinese to match; code comments are Chinese too.

16. **KindEditor keeps only the browser assets** — `static/backend/kindeditor/` retains `kindeditor-all.js`, `plugins`, `themes`, `lang`; the `asp`/`asp.net`/`jsp`/`php` server samples are deleted. Uploads are handled by Django views, not those samples.
