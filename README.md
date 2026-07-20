## 环境
django 5.2， python 3.12 

## 快速启动
```
虚拟环境
virtualenv  venv
启动虚拟环境
source ./venv/bin/activate
安装包
pip install -r requirements.txt
配置数据库
python manage.py migrate
启动django
python manage.py runserver 0.0.0.0:8080
浏览器访问 服务器ip:8080 即可
```


## 可能遇到的问题
1. django.db.utils.OperationalError: no such table: blog_post  
```
输入：
python manage.py  makemigrations blog
python manage.py  makemigrations users
python manage.py migrate 
重新启动服务
python manage.py runserver 
```

## 功能
[功能列表](./docs/开发计划.md)

[修改记录](./docs/changelog.md)

### 感谢
[十分感谢以下资源](./docs/感谢.md)

