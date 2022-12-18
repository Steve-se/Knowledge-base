# from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Post,User,Category, Comment

# Register your models here.

#------------Algorithm for hashing users password-------------------
# class UserAdmin(UserAdmin):
#     pass 

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(User)
