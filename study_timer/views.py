from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import StudySession
from django.contrib import messages

@login_required
def start_timer(request):
    """
    勉強タイマー開始：新たな勉強セッションを作成
    """
    # 既に未終了のセッションがないかチェック
    if StudySession.objects.filter(user=request.user, end_time__isnull=True).exists():
        messages.warning(request, "既にタイマーが動作中です。")
        return redirect('dashboard')
    session = StudySession.objects.create(user=request.user, start_time=timezone.now())
    messages.success(request, "勉強タイマーを開始しました。")
    return redirect('dashboard')

@login_required
def stop_timer(request):
    """
    勉強タイマー停止：未終了のセッションを終了し、勉強時間を記録
    """
    try:
        session = StudySession.objects.get(user=request.user, end_time__isnull=True)
        session.end_time = timezone.now()
        session.save()
        messages.success(request, f"タイマー停止。勉強時間: {session.duration}.")
    except StudySession.DoesNotExist:
        messages.error(request, "動作中のタイマーがありません。")
    return redirect('dashboard')
