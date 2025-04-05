#File Tracking System
A web-based file management and tracking system built using Django, designed to simplify internal file submissions, approvals, and status monitoring between employees and administrators.

#Features:
Employee Panel:
User authentication (login/logout)
Dashboard view with personalized greetings
Upload new file requests
View status of submitted files (Pending, Approved, Rejected)
Change password functionality

Admin Panel:
View list of all employee requests
Approve or reject file submissions
Add new employees from the admin panel
View all employee profiles
Admin dashboard with quick access to requests

General:
Role-based access control (Employee/Admin)
Django admin interface for backend control
Organized templates for clean UI
Static and media file support
Proper directory structure for scalability

Tech Stack:
Backend: Django 5.2
Frontend: HTML, CSS (Bootstrap-based)
Database: SQLite
Deployment-ready: Easily deployable on Vercel or other platforms

Directory Structure Overview
php
Copy
Edit
file-tracking/
├── app/                  # Main Django app with views, models, etc.
├── file_tracking/        # Project settings and configuration
├── templates/            # HTML templates (admin and employee)
├── static/               # Static files (CSS, JS, images)
├── db.sqlite3            # SQLite database
└── manage.py             # Django project management script