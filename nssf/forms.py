# nssf/forms.py
from django import forms
from .models import NSSFDetail, NSSFReturn

class NSSFDetailForm(forms.ModelForm):
    class Meta:
        model = NSSFDetail
        fields = ['nssf_number', 'membership_card']
        widgets = {
            'nssf_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membership_card'].widget.attrs.update({'class': 'form-control'})

class NSSFReturnForm(forms.ModelForm):
    class Meta:
        model = NSSFReturn
        fields = ['month', 'return_file']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['return_file'].widget.attrs.update({'class': 'form-control'})