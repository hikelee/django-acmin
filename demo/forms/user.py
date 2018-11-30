from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, widgets

from acmin.models import User

app_name = __name__.split(".")[0]


def get_user_form():
    class Form(ModelForm):
        class Meta:
            model = User
            fields = User.form_fields

        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop("request", None)
            super().__init__(*args, **kwargs)

        password1 = forms.CharField(
            label='修改密码', min_length=6, max_length=30, help_text=u"如果需要更改密码,请直接填写. 否则就留空",
            widget=forms.PasswordInput, required=False)
        password2 = forms.CharField(
            label='确认密码', min_length=6, max_length=30,
            widget=forms.PasswordInput, required=False)

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and len(password1) > 0 and password1 != password2:
                raise forms.ValidationError("两次密码输入不一致!")
            return password2

    return Form


UserForm = get_user_form()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})
