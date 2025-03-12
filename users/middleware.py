from .models import LoginHistory
from django.utils.deprecation import MiddlewareMixin

class LoginHistoryMiddleware(MiddlewareMixin):
    """
    ログイン後の各リクエストでログイン履歴を記録
    ※ セッションからユーザーをチェックして、初回アクセス時に記録するなど調整可能
    """
    def process_request(self, request):
        if request.user.is_authenticated and not request.session.get('login_recorded', False):
            ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            LoginHistory.objects.create(user=request.user, ip_address=ip, user_agent=user_agent)
            request.session['login_recorded'] = True
