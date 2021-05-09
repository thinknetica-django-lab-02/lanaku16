from rest_framework import serializers

from main.models import Good, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('date_create', 'date_update')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('date_create', 'date_update')


class GoodListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Good
        exclude = ('date_create', 'date_update')


class GoodDetailSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='category_name', read_only=True)
    seller = serializers.SlugRelatedField(slug_field='seller_name', read_only=True)
    tag = serializers.SlugRelatedField(slug_field='tag_name', read_only=True, many=True)

    class Meta:
        model = Good
        fields = ('good_name', 'price', 'good_shifr', 'in_stock', 'category', 'seller', 'tag', 'date_create')


class GoodChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Good
        fields = ('good_name',
                  'description',
                  'price',
                  'discount',
                  'brand',
                  'color',
                  'composition',
                  'good_shifr',
                  'category',
                  'tag',
                  'seller',
                  'in_stock',
                  'picture',
                  'is_published',
                  'archive'
                  )
