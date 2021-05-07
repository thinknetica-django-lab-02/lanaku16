from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class MobileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        subdomain = request.META.get('HTTP_HOST', '').split('.')
        if subdomain == 'm':
            settings.TEMPLATE_DIRS = settings.MOBILE_TEMPLATE_DIRS
        else:
            settings.TEMPLATE_DIRS = settings.DESKTOP_TEMPLATE_DIRS
