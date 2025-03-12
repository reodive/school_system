from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AbsenceNotice
from .forms import AbsenceNoticeForm  # 後述のフォーム

@login_required
def submit_absence_notice(request):
    """
    欠席連絡を送信するビュー
    """
    if request.method == "POST":
        form = AbsenceNoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            messages.success(request, "欠席連絡を送信しました。")
            return redirect('dashboard')
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = AbsenceNoticeForm()
    return render(request, 'attendance/absence_notice_form.html', {'form': form})
