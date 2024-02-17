from rest_framework import permissions


class IsAdminOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Менеджеры').exists()


class IsClient(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.machine.client.user_link == request.user


class IsServiceCompany(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.service_company.user_link == request.user


class IsAdminOrManagerOrClientOrServiceCompany(permissions.BasePermission):

    def has_permission(self, request, view):
        is_admin_or_manager = IsAdminOrManager().has_permission(request, view)
        if is_admin_or_manager:
            return True

        is_client = IsClient().has_permission(request, view)
        if is_client:
            return True

        is_service_company = IsServiceCompany().has_permission(request, view)
        if is_service_company:
            return True

        return False
