from rest_framework import permissions

class CanEditProductPermission(permissions.BasePermission): #if user is a seller not a customer , then he can change the details of his own product delete it
    def has_object_permission(self, request, view, obj):
        return bool(request.user.has_perm('shop.edit_product') and obj.seller == request.user)


class CanCreateProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('shop.add_product')


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)