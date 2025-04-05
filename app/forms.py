from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import EmployeeProfile, File

class EmployeeCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = EmployeeProfile
        fields = ['gender', 'dob', 'designation', 'department', 'mobile']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def save(self, commit=True):
        user_data = {
            'username': self.cleaned_data['email'],
            'email': self.cleaned_data['email'],
            'first_name': self.cleaned_data['name'].split()[0],
            'last_name': ' '.join(self.cleaned_data['name'].split()[1:]) if len(self.cleaned_data['name'].split()) > 1 else '',
        }
        
        user = User.objects.create_user(**user_data, password=self.cleaned_data['password'])
        
        profile = super().save(commit=False)
        profile.user = user
        
        if commit:
            profile.save()
        
        return profile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description', 'file_upload']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_file_upload(self):
        file = self.cleaned_data.get('file_upload')
        if file:
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError("Only PDF or DOC files are allowed.")
        return file
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.uploaded_by = self.user
        
        # Find an assistant engineer to review
        from django.db.models import Q
        from .models import EmployeeProfile
        
        assistant = User.objects.filter(
            profile__designation='assistant',
            profile__department=self.user.profile.department
        ).first()
        
        instance.current_reviewer = assistant
        instance.status = 'pending_assistant'
        
        if commit:
            instance.save()
        
        return instance

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

