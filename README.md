# 全天侯投资者

## About

投资记录及分析，帮助投资者占胜市场。

Python后台程序

## Features

## Technology stack

工具及框架

- [Django](https://www.djangoproject.com) - a python web framework
- [Django REST Framework](http://www.django-rest-framework.org) - a flexible toolkit to build web APIs
- [Django Rest Framework jwt](https://getblimp.github.io/django-rest-framework-jwt/) - a JSON Web Token toolkit for **Django rest framework**

## Requirements

- Use Python 3.x.x+
- Use Django 2.x.x+

## 项目部署

```bash
# 创建虚拟环境
virtualenv virtenv
# 指定虚拟环境
source virtenv/bin/activate
# 安装项目依赖
pip install -r requirements.txt
# 生成数据库迁移文件
python manage.py makemigrations
# 数据库迁移
python manage.py migrate
# 启动项目
nohup python manage.py runserver & disown
```

## Author 作者

[ninemill.song - 九毫](https://github.com/ninemilli-song)

## Reference 参考

- https://github.com/jpadilla/pyjwt - jwt相关

- [Tracking User Login Activity in Django Rest Framework: JWT Authentication](https://medium.com/@atulmishra_69567/tracking-user-login-activity-in-django-rest-framework-jwt-authentication-32e0194e77d0)

- [Let’s build an API with Django REST Framework — Part 2](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-part-2-cfb87e2c8a6c)
