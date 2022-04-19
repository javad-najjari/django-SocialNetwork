from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm



class UserRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].label = ''
    
    image = forms.ImageField(required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email*'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username*'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'name*'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'bio'}))
    website = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'website'}))
    private = forms.BooleanField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password*'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password*'}))
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("this email already exists")
        return email


    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("this username already exists")
        return username


    def clean_password2(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('The passwords must be the same')



class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image',)


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].label = ''

    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search between users'}))


class MessageForm(forms.Form):
    msg_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message...', 'rows': 1, 'cols': 35}), label='')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
