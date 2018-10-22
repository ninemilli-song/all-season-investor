## 创建应用

``` python
python manage.py startapp app
```

## 创建视图

1. app/views.py 添加视图方法
2. app 中创建 urls.py
3. app/urls.py 中添加访问路径
4. ${rootpath}/urls.py 中添加 app/urls.py 中定义的路径

## 数据库配置

修改settings.py：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'all_season_investor',          # 数据库名
        'USER': 'root',                         # 用户名
        'PASSWORD': '19851005',                 # 密码
        'HOST': '127.0.0.1'
    }
}
```

## 其它基本配置

修改settings.py:

```python
LANGUAGE_CODE = 'zh-CN'                 # 设置中文
TIME_ZONE = 'Asia/Shanghai'             # 设置时区
```

## PyCharm中配置MySql

1. 安装驱动
2. 测试

## 初始化数据库

根据settings.py 中的 INSTALLED_APPS 设置初始化数据库

```bash
$ python manage.py migrate
```

## 注册应用

settings.py:
```python
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

## 模型修改三步

### 1. 编辑 models.py

### 2. 生成迁移文件

```bash
$ python manage.py makemigrations app
```

生成了 0001_initial.py 迁移文件

下面的命令可以输出对应迁移文件的sql语句

```bash
$ python manage.py sqlmigrate app 0001
```

### 3. 数据库迁移

执行下面语句进行迁移：

```bash
$ python manage.py migrate
```


## 使用Django API

 使用 manage.py 设置 DJANGO_SETTINGS_MODULE 环境变量，这个变量会让 Django 根据 mysite/settings.py 文件来设置 Python 包的导入路径：

```bash
$ python manage.py shell
```
