
from django.contrib import admin
# from django.urls import re_path as url 
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # url('api/v1/rest-auth/', include('rest_auth.urls')), 

    path('admin/', admin.site.urls),
    path('api/v1/', include('Blog.urls')),
    


    path('api-auth/', include('rest_framework.urls')),#new users can login to the browsable api
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
