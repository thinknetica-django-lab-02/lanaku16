from django.contrib.sitemaps import Sitemap
from main.models import Good


class DynamicViewSitemap(Sitemap):

    def items(self):
        return Good.objects.all()

    def location(self, item):
        return f'/good/{item.pk}/'

    def lastmod(self, item):
        return item.date_create
