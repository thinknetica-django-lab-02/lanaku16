from django.db import models
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from django.utils.html import format_html

from main.models import Good, Tag, Category, Seller


def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


make_published.short_description = "Опубликовать выбранные товары"


def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


make_unpublished.short_description = "Снять с публикации выбранные товары"


def make_archive(modeladmin, request, queryset):
    queryset.update(archive=True)


make_archive.short_description = "Добавить в архив выбранные товары"


def make_unarchive(modeladmin, request, queryset):
    queryset.update(archive=False)


make_unarchive.short_description = "Убрать из архива выбранные товары"


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    actions = [make_published, make_unpublished, make_archive, make_unarchive]
    list_display = (
    'id', 'good_name', 'good_shifr', 'category', 'price', 'seller', 'date_create', 'is_published', 'archive')
    list_display_links = ('good_name',)
    list_filter = ('category', 'date_create', 'is_published', 'archive')
    list_editable = ('is_published', 'archive')
    readonly_fields = ('get_image', 'date_create')
    search_fields = ('good_name', 'good_shifr', 'category__category_name')
    save_as = True
    save_on_top = True

    def get_image(self, obj):
        return format_html('<img src="{}" />'.format(obj.picture.url))

    get_image.short_description = 'Изображение'


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller_name', 'mode', 'boss_name', 'date_create')
    list_display_links = ('seller_name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_name', 'date_create')
    list_display_links = ('tag_name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'slug', 'date_create')
    list_display_links = ('category_name',)


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)

admin.site.site_title = 'Интернет-магазин'
admin.site.site_header = 'Интернет-магазин'
