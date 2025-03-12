from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TimetableEntry

@login_required
def view_timetable(request):
    """
    時間割確認ビュー：ユーザーごとの時間割を表示
    """
    entries = TimetableEntry.objects.filter(user=request.user).order_by('day', 'start_time')
    return render(request, 'timetable/view_timetable.html', {'entries': entries})
