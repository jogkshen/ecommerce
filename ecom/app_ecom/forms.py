from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['fullname', 'address', 'email', 'phone_number', 'order_note']
        # You can customize the widgets or add additional fields as needed
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'order_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

