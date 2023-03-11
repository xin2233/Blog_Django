# Blog_Django
django 3.2， python 3.9  

## 已实现功能
- 博客用户界面
- 登录，注册
- 文章首页显示
- 文章详情显示
- admin管理界面，编辑文章，集成富文本编辑器
- 登录界面优化：增加vanta.js动画，修改登录界面->flatui样式

## 待实现功能
- 忘记密码
- 注册界面样式优化 flatui
- 将admin界面的文章编辑功能，由新增的用户中心界面的文章编辑按钮，跳转到自实现的新的文章编辑界面，不在使用admin的默认编辑功能
- 增加后端文章管理页面的编辑功能，可以直接编辑文章，参考django admin 系统设置或者博客园的文章修改页面
- 

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

### 感谢
[十分感谢以下资源](./docs/感谢.md)

