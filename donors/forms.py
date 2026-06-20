from django import forms
from .models import Donor

class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['blood_group', 'date_of_birth', 'last_donation_date', 'is_available']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }
