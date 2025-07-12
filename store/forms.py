from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import ShippingAddress

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'KullanıcıAdı'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}),
             'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Şifre Tekrar'}),
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address','city','postal_code']        
