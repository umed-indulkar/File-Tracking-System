from django.contrib import admin
from .models import EmployeeProfile, File, ApprovalHistory

# Register your models with the admin site
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'department', 'gender', 'mobile')
    list_filter = ('designation', 'department', 'gender')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'department')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'status', 'date_uploaded')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'uploaded_by__username')
    date_hierarchy = 'date_uploaded'

@admin.register(ApprovalHistory)
class ApprovalHistoryAdmin(admin.ModelAdmin):
    list_display = ('file', 'approved_by', 'status', 'approved_at')
    list_filter = ('status',)
    search_fields = ('file__title', 'approved_by__username')
    date_hierarchy = 'approved_at'

