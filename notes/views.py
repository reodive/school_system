from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NoteForm
from .models import Note

@login_required
def create_note(request):
    """
    ノート作成ビュー：新規にデジタルノートを作成する
    """
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            messages.success(request, "ノートが作成されました。")
            return redirect('note_detail', note_id=note.id)
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_detail(request, note_id):
    """
    ノート詳細ビュー：作成したノートの内容を表示する
    """
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})
