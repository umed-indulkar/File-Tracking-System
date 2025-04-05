from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EmployeeProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    DESIGNATION_CHOICES = (
        ('assistant', 'Assistant Engineer'),
        ('deputy', 'Deputy Engineer'),
        ('executive', 'Executive Engineer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    department = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_designation_display()}"

class File(models.Model):
    STATUS_CHOICES = (
        ('pending_assistant', 'Pending Approval (Assistant)'),
        ('pending_deputy', 'Pending Approval (Deputy)'),
        ('pending_executive', 'Pending Approval (Executive)'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_upload = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_assistant')
    current_reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='files_to_review')
    date_uploaded = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class ApprovalHistory(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='approvals')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=(('approved', 'Approved'), ('rejected', 'Rejected')))
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.file.title} - {self.status} by {self.approved_by.get_full_name()}"

