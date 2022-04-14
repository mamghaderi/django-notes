from rest_framework import permissions


# By overriding the BasePermission class, we can create our own permission.
# This class has two methods that we can override.
# .has_permission() and .has_object_permission()
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPublicReadOnly(permissions.BasePermission):
    """
    Custom permission to return just public objects.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.public:
            return True


# class IsOwnerOrPublicReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it, except public objects in safe methods.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS and obj.public:
#             return True
#
#         # Write permissions are only allowed to the owner of the snippet.
#         return obj.owner == request.user
