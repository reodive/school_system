from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# 既存のログインフォーム
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ユーザー名'
        })
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワード'
        })
    )

# カスタムユーザー登録フォーム
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # カスタムユーザーモデルに合わせて必要なフィールドを指定します。
        # 例: username, email, role (ユーザーの役割) など
        fields = ('username', 'email', 'role')
        
    # 必要に応じて、フィールドのウィジェットやバリデーションのカスタマイズも可能です。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 各フィールドにBootstrapのCSSクラスを追加する例
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ユーザー名'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'メールアドレス'
        })
        self.fields['role'].widget.attrs.update({
            'class': 'form-control',
        })
        # パスワードフィールドも同様に
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード（確認）'
        })
