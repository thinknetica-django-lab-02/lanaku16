from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('goods', views.GoodListView.as_view(), name='goods'),
    path('goods/<int:pk>', views.GoodDetailView.as_view(), name='good-detail'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    #path('accounts/profile/<int:pk>', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('accounts/profile/<int:pk>', views.update_profile, name='update_profile'),
]
