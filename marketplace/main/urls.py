from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('goods', views.GoodListView.as_view(), name='goods'),
    path('goods/<int:pk>', views.GoodDetailView.as_view(), name='good-detail'),
    path('goods/add', views.GoodAddView.as_view(), name='good-add'),
    path('goods/<int:pk>/edit', views.GoodUpdateView.as_view(), name='good-update'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('accounts/profile/<int:pk>', views.update_profile, name='update-profile'),
    path('accounts/login', views.login, name='login'),
]
