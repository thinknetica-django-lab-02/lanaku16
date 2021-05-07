from django.urls import path
from main.sitemap import DynamicViewSitemap
from django.contrib.sitemaps.views import sitemap

from . import views

sitemaps = {
    'dynamic': DynamicViewSitemap
}

urlpatterns = [
    path('', views.index, name='home'),
    path('goods', views.GoodListView.as_view(), name='goods'),
    path('goods/<int:pk>', views.GoodDetailView.as_view(), name='good-detail'),
    path('goods/add', views.GoodAddView.as_view(), name='good-add'),
    path('goods/<int:pk>/edit', views.GoodUpdateView.as_view(), name='good-update'),
    path('search', views.Search.as_view(), name='search'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('delivery', views.delivery, name='delivery'),
    path('pay', views.pay, name='pay'),
    path('accounts/profile/<int:pk>', views.update_profile, name='update-profile'),
    path('accounts/register', views.RegisterUser.as_view(), name='register'),
    path('accounts/login', views.LoginUser.as_view(), name='login'),
    path('accounts/logout', views.logout_user, name='logout'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

]
