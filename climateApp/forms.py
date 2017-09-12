from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Terminal, City


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={"placeholder": "请输入用户名"}))
    password = forms.CharField(label='密 码', widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}))
    checkcode = forms.CharField(label='验证码', widget=forms.TextInput(attrs={"placeholder": "请输入验证码","pattern":"\w{4}"}))

    # def clean_check_code(self):
    #     cd = self.cleaned_data
    #     if len(cd['check_code']) < 4:
    #         raise forms.ValidationError('code must be 4 characters')
    #     return cd['check_code']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        #From User fields
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        '''Check if both password matches'''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if not email:
            raise forms.ValidationError('Email address is required')

        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email address has already be registered')
        return email

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('displayName', 'mobile', 'photo')



class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.cityName

class DevForm(forms.ModelForm):

    #deviceEui = forms.CharField(max_length=20, label='设备编号')
    deviceAddr = MyModelChoiceField(queryset=City.objects.all())
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"readonly":True}))
    class Meta:
        model = Terminal
        fields = ('deviceEui', 'deviceAddr', 'username')