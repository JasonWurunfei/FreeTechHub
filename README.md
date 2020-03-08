# Free Tech Hub

---

> **Requirements**

- Python 3.8
- Django 3.0.3

---
> **About make index file **
- cmd:python manage.py rebuild_index, make index file "whoosh_index/"
> **About sign up with email **
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
- if you do not want to use this function
program annotation  modify    `accounts/views.py` ，as follows: 
```bash
 if form.is_valid():
              form.save()
          #  user = form.save()
         #    user.refresh_from_db()
         #   user.profile.username = form.cleaned_data.get('username')
         #   user.profile.email = form.cleaned_data.get('email')
         #   user.is_active = False
         #  user.save()
         #  current_site = get_current_site(request)
         #  subject = 'Please Activate Your Account'
         #  message = render_to_string('registration/activation_request.html', {
         #       'user': user,
         #      'domain': current_site.domain,
         #      'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        #  })
       #  user.email_user(subject, message)
            return redirect("accounts:activation_sent")
```

