from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated


class IsEntityManager(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return super().has_permission(request, view)

        return False


class IsActiveUser(IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not request.user.is_active:
            return False
        if not request.user.email_verified:
            return False
        return super().has_permission(request, view)
