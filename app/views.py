from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import EmployeeProfile, File, ApprovalHistory
from .forms import EmployeeCreationForm, FileUploadForm, CustomPasswordChangeForm

def is_admin(user):
    return user.is_superuser

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('employee_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

# Admin views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin/admin_home.html')

@login_required
@user_passes_test(is_admin)
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect('view_employees')
    else:
        form = EmployeeCreationForm()
    return render(request, 'admin/add_employee.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def view_employees(request):
    employees = EmployeeProfile.objects.all()
    return render(request, 'admin/view_employees.html', {'employees': employees})

# Employee views
@login_required
def employee_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'employee/dashboard.html')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "File uploaded successfully and sent for approval.")
            return redirect('view_status')
    else:
        form = FileUploadForm()
    return render(request, 'employee/upload_file.html', {'form': form})

@login_required
def view_requests(request):
    user_profile = request.user.profile
    
    # Get files that this user needs to review based on designation
    if user_profile.designation == 'assistant':
        files = File.objects.filter(status='pending_assistant', current_reviewer=request.user)
    elif user_profile.designation == 'deputy':
        files = File.objects.filter(status='pending_deputy', current_reviewer=request.user)
    elif user_profile.designation == 'executive':
        files = File.objects.filter(status='pending_executive', current_reviewer=request.user)
    else:
        files = File.objects.none()
    
    return render(request, 'employee/view_requests.html', {'files': files})

@login_required
def view_status(request):
    files = File.objects.filter(uploaded_by=request.user)
    return render(request, 'employee/view_status.html', {'files': files})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password was successfully updated!")
            return redirect('employee_dashboard')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'employee/change_password.html', {'form': form})

@login_required
def approve_reject_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comments = request.POST.get('comments', '')
        
        if action not in ['approve', 'reject']:
            messages.error(request, "Invalid action.")
            return redirect('view_requests')
        
        # Record the approval/rejection
        ApprovalHistory.objects.create(
            file=file,
            approved_by=request.user,
            status='approved' if action == 'approve' else 'rejected',
            comments=comments
        )
        
        if action == 'reject':
            file.status = 'rejected'
            file.current_reviewer = None
            file.save()
            messages.success(request, "File has been rejected.")
            return redirect('view_requests')
        
        # If approved, move to next level
        user_profile = request.user.profile
        
        if user_profile.designation == 'assistant':
            # Find a deputy engineer to review
            deputy = User.objects.filter(
                profile__designation='deputy',
                profile__department=user_profile.department
            ).first()
            
            if deputy:
                file.status = 'pending_deputy'
                file.current_reviewer = deputy
            else:
                messages.error(request, "No deputy engineer found to review this file.")
                return redirect('view_requests')
                
        elif user_profile.designation == 'deputy':
            # Find an executive engineer to review
            executive = User.objects.filter(
                profile__designation='executive',
                profile__department=user_profile.department
            ).first()
            
            if executive:
                file.status = 'pending_executive'
                file.current_reviewer = executive
            else:
                messages.error(request, "No executive engineer found to review this file.")
                return redirect('view_requests')
                
        elif user_profile.designation == 'executive':
            # Final approval
            file.status = 'approved'
            file.current_reviewer = None
            
        file.save()
        messages.success(request, "File has been approved and moved to the next stage.")
        return redirect('view_requests')
        
    return render(request, 'employee/approve_reject.html', {'file': file})

