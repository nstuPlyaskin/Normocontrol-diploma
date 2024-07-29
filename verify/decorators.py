from functools import wraps

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

User = get_user_model()


def user_check(func):
    """Декоратор. Проверяет доступность страницы для текущего пользователя."""
    @wraps(func)
    def wrap(request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        if request.user != user:
            raise PermissionDenied
        return func(request, *args, **kwargs)
    return wrap


def user_access(func):
    """Декоратор. Проверяет наличие прав нормоконтроллера."""
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if not request.user.allow_manage:
            raise PermissionDenied
        return func(request, *args, **kwargs)
    return wrap
