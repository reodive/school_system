from django import forms
from .models import AbsenceNotice

class AbsenceNoticeForm(forms.ModelForm):
    class Meta:
        model = AbsenceNotice
        fields = ['date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
