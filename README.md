# 全天侯投资者

## About

投资记录及分析，帮助投资者占胜市场。

Python后台程序

## 技术栈（Technology stack）

技术 | 说明 | 网址
--- | --- | ---
Python | 编程语言 | [https://www.python.org/](https://www.python.org/)
Django | Python Web 框架 | [https://www.djangoproject.com](https://www.djangoproject.com)
Django REST Framework | 构造REST api的工具框架 | [http://www.django-rest-framework.org](http://www.django-rest-framework.org)
Django Rest Framework jwt | 基于DRF的JWT认证框架 | [https://getblimp.github.io/django-rest-framework-jwt/](https://getblimp.github.io/django-rest-framework-jwt/)

## Requirements

- Use Python 3.x.x+
- Use Django 2.x.x+

## 开发环境搭建

1. 使用PyCharm创建Django工程

2. 克隆代码到工程根目录

```bash
cd ***
git clone git@github.com:ninemilli-song/all-season-investor.git
```

3. 设置Project interpreter目录为 **venv** 目录

> Preferences -> Project -> Project interpreter

4. 自动安装requirements.txt中的指定依赖

5. **run** or **debug**

## 生产环境部署

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

### 许可（License）

Copyright (c) [ninemilli.song](https://github.com/ninemilli-song)

[MIT License][MIT]

[MIT]: ./LICENSE "Mit License"