# dm/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from users.models import CustomUser
from .models import GroupChatRoom, GroupChatMessage
from .forms import GroupChatMessageForm

@login_required
def group_chat_room_list(request):
    """
    ユーザーが参加しているグループチャットルームの一覧を表示するビュー
    """
    rooms = request.user.chat_rooms.all()
    return render(request, 'dm/group_chat_room_list.html', {'rooms': rooms})

@login_required
def group_chat_room_detail(request, room_id):
    """
    指定したグループチャットルームのメッセージ履歴を表示し、新規メッセージを送信できるビュー
    """
    room = get_object_or_404(GroupChatRoom, pk=room_id)
    # 参加していない場合はアクセスを拒否（オプション）
    if request.user not in room.members.all():
        messages.error(request, "このチャットルームにはアクセスできません。")
        return redirect('group_chat_room_list')

    messages_qs = room.messages.all().order_by('created_at')
    if request.method == 'POST':
        form = GroupChatMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.room = room
            msg.sender = request.user
            msg.save()
            messages.success(request, "メッセージが送信されました。")
            return redirect('group_chat_room_detail', room_id=room.id)
        else:
            messages.error(request, "メッセージ送信に失敗しました。")
    else:
        form = GroupChatMessageForm()

    return render(request, 'dm/group_chat_room_detail.html', {
        'room': room,
        'messages_qs': messages_qs,
        'form': form,
    })

@login_required
def message_list(request):
    """
    ログインユーザーに関連する受信・送信メッセージ一覧を表示。
    1対1チャット相手の一覧を簡易的に表示する例。
    """
    # 自分がやり取りした相手の一覧を取得
    sent_user_ids = request.user.sent_messages.values_list('receiver', flat=True)
    received_user_ids = request.user.received_messages.values_list('sender', flat=True)
    user_ids = set(sent_user_ids) | set(received_user_ids)  # 和集合
    users = CustomUser.objects.filter(id__in=user_ids)

    return render(request, 'dm/message_list.html', {
        'users': users,
    })

@login_required
def message_detail(request, user_id):
    """
    特定の相手(user_id)とのDMを表示し、新規メッセージ送信を行う。
    """
    other_user = get_object_or_404(CustomUser, pk=user_id)
    # 自分と相手のやり取りのみ抽出
    messages_qs = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('message_detail', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'dm/message_detail.html', {
        'other_user': other_user,
        'messages_qs': messages_qs,
        'form': form
    })
