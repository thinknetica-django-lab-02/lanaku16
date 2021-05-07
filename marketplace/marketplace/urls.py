"""marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

from marketplace import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', RedirectView.as_view(url='main/', permanent=True)),
    path('accounts/', include('allauth.urls')),
    path('chat/', include('chat.urls')),
    path('api/v1/', include('api.urls')),
    path('api/v1/', include('rest_framework.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
