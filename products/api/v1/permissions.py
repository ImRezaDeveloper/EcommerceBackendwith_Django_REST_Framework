from products.models import CommentProduct, User
from rest_framework.permissions import BasePermission

class IsOwnerForEdit(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user