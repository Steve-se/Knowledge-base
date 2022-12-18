from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .authentications import Register, ChangePassword

urlpatterns = [
    #CATEGORIES
    path('category/', CategoryList.as_view(), name='category'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),

    #POSTS
    path('post/', PostList.as_view(), name='post'),
    path('post/<int:pk>/', PostDetail.as_view(), name= 'post_detail'),
    
    #USER
    path('user/', UserList.as_view(), name='user'),
    path('user/<int:pk>/', UserDetail.as_view(), name= 'user_detail'),

    #COMMENTS
    path('comment/', CommentList.as_view()),
    path('comment/<int:pk>/', CommentDetail.as_view()),

    #jwt authentication path
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', Register.as_view(), name='register'),
    path('change_password/<int:pk>', ChangePassword.as_view(), name='change password'),
]
