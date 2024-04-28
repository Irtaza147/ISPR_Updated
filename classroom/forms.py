from django.forms.utils import ValidationError
from classroom.models import User, Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer,User
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth import get_user_model
from django.core.signals import setting_changed
from django.dispatch import receiver
from .models import ImageUploadForm
from .models import Firmware
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom User model

class SignupForm(UserCreationForm):
    role_choices = [
        ('vendor', 'Vendor'),
        ('regular', 'Regular User'),
    ]

    role = forms.ChoiceField(choices=role_choices, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different one.')
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        # Add your password strength validation logic here
        # For example, you can check for a minimum length, uppercase, lowercase, and numbers
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']








class Imageform(forms.ModelForm):
    class Meta:
        model=ImageUploadForm
        fields='__all__'


class FirmwareForm(forms.ModelForm):
    class Meta:
        model = Firmware
        fields = ['name', 'device_model', 'current_version', 'firmware_file']
    
    widgets = {
        'name': forms.TextInput(attrs={'placeholder': 'Enter Firmware Name'}),
        'device_model': forms.TextInput(attrs={'placeholder': 'Enter Device Model'}),
        'current_version': forms.TextInput(attrs={'placeholder': 'Enter Current Version'}),
    }
    # This makes the firmware_file field optional
    firmware_file = forms.FileField(required=False)


class CustomerForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['car_model'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['car_color'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['cost_per_day'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['phone_number'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['comment'].widget.attrs = {
            'class': 'form-control col-md-6'
        } 
        self.fields['is_payed'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'car_model', 'car_color', 'cost_per_day', 'phone_number', 'comment', 'is_payed')




class UserForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control col-md-6'
        }


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


