from django import forms
from .models import Hospital

class HospitalProfileForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'registration_number','phone','city', 'icu_beds', 'oxygen_beds', 'general_beds']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'icu_beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'oxygen_beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'general_beds': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from .models import HospitalReview

class HospitalReviewForm(forms.ModelForm):
    class Meta:
        model = HospitalReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review here...'}),
        }
