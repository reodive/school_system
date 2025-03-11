# calendarapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CalendarEvent

@login_required
def calendar_view(request):
    """
    カレンダー表示ページ（FullCalendarのHTML）
    """
    return render(request, 'calendarapp/calendar.html')

@login_required
def calendar_events(request):
    """
    FullCalendar用のイベント一覧をJSONで返す。
    """
    events = CalendarEvent.objects.all()  # ここでは全イベントを返す例
    data = []
    for e in events:
        data.append({
            'id': e.id,
            'title': e.title,
            'start': e.start.isoformat(),
            'end': e.end.isoformat() if e.end else None,
            'description': e.description,
        })
    return JsonResponse(data, safe=False)
