from rest_framework import permissions

from shop.models import Product

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

class CanAddImageToProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        product_id = view.kwargs['product_pk']
        product = Product.objects.select_related('seller').get(id=product_id)
        return bool(request.user == product.seller and request.user.has_perm('shop.edit_product'))


class CanEditImageRelatedToAProductPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.has_perm('shop.edit_product') and obj.product.seller == request.user)