from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import HTTP_200_OK

from main.models import Good, Category, Tag
from .permissions import IsGoodOwner

from .serializers import \
    GoodListSerializer, \
    GoodDetailSerializer, \
    GoodChangeSerializer, \
    CategorySerializer, \
    TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.get_all_tags(Tag)
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag_name']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif action == 'retrive':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.get_all_categories(Category)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_name']

    def getcounts(self, request, pk, *args, **kwargs):
        return Response({
            'category': pk,
            'goodscount': Category.get_count_goods_in_category(Category,pk)
        }, status=HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif action == 'retrive':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]


class GoodViewSet(viewsets.ViewSet):
    filterset_fields = ('category',
                        'in_stock',
                        'is_published',
                        'seller',
                        'archive',
                        'date_create')

    def get_queryset(self):
        return Good.get_all_goods(Good)

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif action == 'retrive':
            permission_classes = [permissions.IsAuthenticated]
        elif action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [IsGoodOwner]

        return [permission() for permission in permission_classes]

    def list(self, request):
        query_set = Good.get_all_goods(Good)
        serializer = GoodListSerializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response(serializer.data)

    def retrive(self, request, pk=None):
        query_set = Good.get_all_goods(Good)
        good = get_object_or_404(query_set, pk=pk)
        serializer = GoodDetailSerializer(good)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        query_set = Good.get_all_goods(Good)
        good = get_object_or_404(query_set, pk=pk)
        good.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        query_set = Good.get_all_goods(Good)
        good = get_object_or_404(query_set, pk=pk)
        serializer = GoodChangeSerializer(data=request.data)
        if serializer.is_valid():
            good.save()
            return Response(serializer.data)

        return Response({
            'status': 'Bad request',
            'message': 'Good could not be svaed with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = GoodChangeSerializer(data=request.data)
        if serializer.is_valid():
            Good.objects.create(**serializer.validated_data)
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Good could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)