from ast import BinOp
from distutils.command.upload import upload
from email.mime import image
from enum import unique
from django.db import models
from .fields import CaseInsensitiveCharField
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.
'''
4 models
----- users
----- category
----- post
----- comment
'''

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=True)
    email =  models.EmailField(unique=True, max_length=250)
    username = CaseInsensitiveCharField(max_length=250, unique=True) 
    user_image = models.ImageField(upload_to='blog/user_image/', null=True, blank=True)
    bio = models.CharField(max_length=350)
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
            swappable = 'AUTH_USER_MODEL' 

    def __str__(self):
        return self.username

    

class Category(models.Model):
    name= CaseInsensitiveCharField(max_length=150, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    intro = models.CharField(max_length=1000)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/images', null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    resources = models.FileField(upload_to='blog/resources/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.resources.delete()
        super().delete(*args, **kwargs)   

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'posts'

class Comment(models.Model):
    '''
    Who made the comment, to which post, and what is the comment
    '''
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.comment

