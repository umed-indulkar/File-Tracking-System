from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Admin pages
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add-employee/', views.add_employee, name='add_employee'),
    path('admin/view-employees/', views.view_employees, name='view_employees'),
    
    # Employee pages
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/upload-file/', views.upload_file, name='upload_file'),
    path('employee/view-requests/', views.view_requests, name='view_requests'),
    path('employee/view-status/', views.view_status, name='view_status'),
    path('employee/change-password/', views.change_password, name='change_password'),
    path('employee/file/<int:file_id>/review/', views.approve_reject_file, name='approve_reject_file'),
]

