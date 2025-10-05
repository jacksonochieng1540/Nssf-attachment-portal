from django import forms
from .models import Attachment, Company, StudentProfile
from accounts.models import User  # Import User model

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['company', 'start_date', 'end_date', 'supervisor_name', 'supervisor_email', 'supervisor_phone']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'supervisor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisor_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'supervisor_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        
        # Customize company field based on user role
        self.fields['company'] = forms.ModelChoiceField(
            queryset=Company.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            empty_label="Select Company"
        )
        
        # If user is a company, only show their company
        if user.role == 'company':
            try:
                company = Company.objects.get(user=user)
                self.fields['company'].queryset = Company.objects.filter(id=company.id)
                self.fields['company'].initial = company
            except Company.DoesNotExist:
                self.fields['company'].queryset = Company.objects.none()
        
        # If user is a student, show all companies
        elif user.role == 'student':
            self.fields['company'].queryset = Company.objects.all()
        
        # If user is admin, show all companies
        elif user.role == 'admin':
            self.fields['company'].queryset = Company.objects.all()
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data

# Form for admin to create companies and assign users
class AdminCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['user', 'name', 'address', 'nssf_number']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nssf_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users who don't already have a company and are not students
        existing_company_users = Company.objects.values_list('user_id', flat=True)
        self.fields['user'].queryset = User.objects.exclude(
            id__in=existing_company_users
        ).exclude(role='student')
        self.fields['user'].empty_label = "Select User"
    
    def clean_nssf_number(self):
        nssf_number = self.cleaned_data.get('nssf_number')
        if nssf_number and Company.objects.filter(nssf_number=nssf_number).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError("A company with this NSSF number already exists.")
        return nssf_number

# Form for users to register their own company
class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'nssf_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nssf_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_nssf_number(self):
        nssf_number = self.cleaned_data.get('nssf_number')
        if nssf_number and Company.objects.filter(nssf_number=nssf_number).exists():
            raise forms.ValidationError("A company with this NSSF number already exists.")
        return nssf_number

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'department']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if student_id and StudentProfile.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("A student with this ID already exists.")
        return student_id

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'  # Or specify specific fields like ['field1', 'field2', ...]
        exclude = ['user']  # 