from django.contrib.auth import password_validation
from store.models import Address
from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _
from .models import CustomizationInquiry


class SortForm(forms.Form):
    SORT_CHOICES = [
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
    ]
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'pin_code', 'state']
        widgets = {
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your House Name / Flat.No / Work'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Pincode'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State or Province'})
        }


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'auto-focus':True, 'class':'form-control', 'placeholder':'Current Password'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control', 'placeholder':'Confirm Password'}))


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))



# custmization form for the customer



class CustomizationInquiryForm(forms.ModelForm):
    class Meta:
        model = CustomizationInquiry
        fields = ['name', 'product_name', 'email', 'mobile', 'message']
