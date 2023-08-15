from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


# 사용자 생성 폼
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        # 아래 수정 예정
        fields = ('user_id', 'profile_nickname', 'profile_image', 'account_email')

    # 패스워드 일치 검증
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# 사용자 수정 폼
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('user_id', 'profile_nickname', 'profile_image', 'account_email', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]