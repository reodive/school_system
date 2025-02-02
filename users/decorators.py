# users/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    """
    ユーザーの role が allowed_roles に含まれている場合にのみビューにアクセスを許可するデコレーター。
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("この操作を行う権限がありません。")
        return _wrapped_view
    return decorator
