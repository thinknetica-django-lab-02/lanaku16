from django.urls import path

from . import api



urlpatterns = [
    path('goods-set/', api.GoodViewSet.as_view({'get': 'list',
                                                'post': 'create'})),
    path('goods-set/<int:pk>', api.GoodViewSet.as_view({'get': 'retrive',
                                                        'put': 'update',
                                                        'delete': 'destroy'})),
    ]
