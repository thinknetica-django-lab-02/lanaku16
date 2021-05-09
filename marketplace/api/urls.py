from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import api


router = DefaultRouter()
router.register(r'category-modelset', api.CategoryViewSet, basename='category')
router.register(r'tag-modelset', api.TagViewSet, basename='tag')

urlpatterns = [
    path('goods-set/', api.GoodViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('goods-set/<int:pk>', api.GoodViewSet.as_view({
        'get': 'retrive',
        'put': 'update',
        'delete': 'destroy'
    })),
    ]

urlpatterns += router.urls
urlpatterns += format_suffix_patterns([
    path('category-modelset/<int:pk>/goodscount/',
         api.CategoryViewSet.as_view({'get': 'getcounts'}),
         name='goodscount')
])

