# dm/forms.py
from django import forms
from .models import Message
from .models import GroupChatMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class GroupChatMessageForm(forms.ModelForm):
    class Meta:
        model = GroupChatMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'メッセージを入力してください'}),
        }
