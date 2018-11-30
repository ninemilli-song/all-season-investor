# 全天侯投资者

## About

投资记录及分析，帮助投资者占胜市场。

Python后台程序

## Features

## Technology stack

工作及框架

- [Django](https://www.djangoproject.com) - a python web framework
- [Django REST Framework](http://www.django-rest-framework.org) - a flexible toolkit to build web APIs
- [Django Rest Framework jwt](https://getblimp.github.io/django-rest-framework-jwt/) - a JSON Web Token toolkit for **Django rest framework**

## Requirements

- Use Python 3.x.x+
- Use Django 2.x.x+

## Running the application

```bash
virtualenv virtenv
source virtenv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
nohup python manage.py runserver & disown
```

## Author 作者

[ninemill.song](https://github.com/ninemilli-song)

## Thanks 感谢

Open source project:

- https://github.com/jpadilla/pyjwt - jwt相关

Blog:

- https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-part-2-cfb87e2c8a6c - jwt相关
