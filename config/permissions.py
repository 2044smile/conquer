from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자에게만 쓰기 권한을 부여합니다.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용됩니다.
        # 따라서 GET, HEAD, OPTIONS 요청은 항상 허용됩니다.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 `Snippet`의 소유자에게만 허용됩니다.
        return obj.owner == request.user