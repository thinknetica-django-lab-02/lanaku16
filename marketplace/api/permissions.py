from rest_framework import permissions

from main.models import Seller

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        seller = Seller.get_user_id(obj.seller)
        return seller == request.user