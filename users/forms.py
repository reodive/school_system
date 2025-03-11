# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import NotificationSetting

class NotificationSettingForm(forms.ModelForm):
    class Meta:
        model = NotificationSetting
        fields = ['assignment_reminder', 'chat_notification', 'announcement_notification', 'reminder_frequency']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]

# カスタムログインフォーム
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ユーザー名',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワード',
            'autocomplete': 'current-password'
        })
    )
    
    # ※ 必要に応じて clean メソッドなどをオーバーライドして、
    #     入力値のバリデーションやカスタムエラーメッセージを追加することも可能です。

# カスタムユーザー登録フォーム
class CustomUserCreationForm(UserCreationForm):
    # 必要に応じて、email フィールドを必須にする例
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'メールアドレス'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 共通のウィジェットクラスを追加し、視認性を向上させます。
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ユーザー名'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'メールアドレス'
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-select',  # role は選択肢フィールドの場合、form-select を使用するのが適切
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード（確認）'
        })
        
        # 各フィールドのラベルやヘルプテキストをカスタマイズする場合の例
        self.fields['username'].label = "ユーザー名"
        self.fields['email'].label = "メールアドレス"
        self.fields['role'].label = "ユーザーの役割"
        self.fields['password1'].label = "パスワード"
        self.fields['password2'].label = "パスワード確認"

        # さらに、エラー発生時の表示用にエラークラスの設定が必要な場合は、
        # テンプレート側で form.errors を確認し、Bootstrap の alert クラスなどを利用するのがおすすめです。
