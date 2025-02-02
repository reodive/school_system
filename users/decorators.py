# users/decorators.py (例)

from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # ログイン画面へ
            
            if request.user.role not in allowed_roles:
                # ロールが許可されていない場合、トップやエラーへ
                return redirect('home')  # または 403 Forbidden にする
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
