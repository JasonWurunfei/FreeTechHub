# Free Tech Hub

---

> **Requirements**

- Python 3.8
- Django 3.0.3

##About make index file 
- cmd:python manage.py rebuild_index, make index file "whoosh_index/"
---
##About sign up with email About sign up with email
-  Start the SMTP service（Such as QQ, 163 ........)
-  To configure the setting.py
modify   `FTH/setting.py` ，as follows:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = True 
EMAIL_HOST = ['smtp.163.com'or  'smtp.qq.com'.......]#Choose whatever you use
EMAIL_PORT = 465   #Port number
EMAIL_HOST_USER = ' EMAIL_HOST'       # 我自己的邮箱
EMAIL_HOST_PASSWORD = ''       # 我的邮箱授权码
EMAIL_SUBJECT_PREFIX = '[FREETECHHUB]'     # 为邮件Subject-line前缀,默认是'[django]'
```

## If you want to test the login function
1. Complete the previous step
1. Log in to your GitHub account, go to Settings. In the left menu you will see Developer settings. Click on OAuth applications.In the OAuth applications screen click on Register a new application. Or simply click on the link below:
 https://github.com/settings/applications/new

 Provide the information below:
 ![avatar](/image/readme/1.png)
1. After hitting the "Register application" button you'll be redirected to the following page.
![avatar](/image/readme/2.png)
1. We need to configure the admin portion of our Django project. Create a new superuser so we can login! Follow the prompts after typing the command below:
```bash
./python manage.py createsuperuser
```
Now we can start the server again with `python manage.py runserver` and then navigate to the admin page http://127.0.0.1:8000/admin. Use your newly-created superuser credentials to login.

The admin homepage should look like this now:
![avatar](/image/readme/3.png)
# And then you can follow this blog 
## By reading this blog, you will know how to complete it
https://www.jianshu.com/p/8989be98fd6d
