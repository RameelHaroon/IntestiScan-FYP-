from django import forms
from .models import User, Image
from django.forms import Textarea, TextInput, EmailInput, PasswordInput

class UserSignInForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

     # Define form attributes
    def __init__(self, *args, **kwargs):
        super(UserSignInForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'Userform'})
        self.fields['password'].widget.attrs.update({'class': 'Userform'})


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'name': TextInput(attrs={
                'class': "Userform",
                }),
            'email': EmailInput(attrs={
                'class': "Userform",
                }),
            'password': TextInput(attrs={
                'class': "Userform",
                })
        }
        labels = {
            'name' : 'Name',
            'email' : 'Email',
            'password' : 'Password',
        }
        label_class = 'label-class'

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError()
            return email

        def clean_password(self):
            password = self.cleaned_data.get('password')
            if len(password) < 8:
                raise forms.ValidationError()
            return password
        
        # Customize error messages for fields
        error_messages = {
            'name': {
                'required': "Please enter your name.",
            },
            'email': {
                'required': "Please enter your email address.",
                'invalid': "Please enter a valid email address.",
                'unique': "This email address is already in use"
            },
            'password': {
                'required': "Please enter a password.",
                'min_length': "Password must be at least 8 characters long.",
                'max_length': 'Password must be less than 16 characters long.'
            },
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']