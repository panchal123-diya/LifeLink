from django import forms
from .models import BloodBank

class BloodBankProfileForm(forms.ModelForm):
    class Meta:
        model = BloodBank
        exclude = ('user', 'is_verified', 'created_at', 'updated_at')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'a_pos': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'a_neg': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'b_pos': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'b_neg': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'ab_pos': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'ab_neg': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'o_pos': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'o_neg': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        }
