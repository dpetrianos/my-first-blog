from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime

# AUTH_USER_MODEL = 'blog.User'

class Post(models.Model):
    # print(AUTH_USER_MODEL)     
    # print(auth.User)
   
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)   # default = datetime.now
    published_date = models.DateTimeField(blank=True, null=True)
    # ncomments = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


# class User(models.Model):
#     username = models.CharField(max_length=150)
#     password = models.CharField(max_length=128, blank=False)
#     email = models.EmailField(max_length=128)
#     mobile = models.CharField(max_length=20)
#     is_superuser = models.BooleanField(blank=False, default=True)

#     def __str__(self):
#         return self.username
        
    # EMAIL_FIELD
    # A string describing the name of the email field on the User model. 
    # This value is returned by get_email_field_name().

