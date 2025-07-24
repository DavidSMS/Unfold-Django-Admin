from django.contrib.admin import AdminSite
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User


def environment_callback(request):
    """
    Callback to determine the environment for the admin interface.
    This will show an environment indicator in the admin.
    """
    from django.conf import settings
    
    if settings.DEBUG:
        return ["🔧 Development", "warning"]
    return ["🚀 Production", "success"]


def dashboard_callback(request, context):
    """
    Callback to customize the admin dashboard with HR-specific widgets and statistics.
    """
    from hr.models import Employee, Department, LeaveRequest, Attendance
    
    # Get current date and calculate date ranges
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    current_year_start = today.replace(month=1, day=1)
    
    # Employee Statistics
    total_employees = Employee.objects.filter(is_active=True).count()
    active_employees = Employee.objects.filter(
        employment_status='ACTIVE', 
        is_active=True
    ).count()
    new_hires_this_month = Employee.objects.filter(
        hire_date__gte=current_month_start,
        is_active=True
    ).count()
    employees_on_leave = Employee.objects.filter(
        employment_status='ON_LEAVE',
        is_active=True
    ).count()
    
    # Department Statistics
    departments_with_employees = Department.objects.annotate(
        emp_count=Count('employees', filter=Q(employees__is_active=True))
    ).filter(emp_count__gt=0).count()
    
    # Leave Request Statistics
    pending_leave_requests = LeaveRequest.objects.filter(
        status='PENDING'
    ).count()
    
    approved_leaves_this_month = LeaveRequest.objects.filter(
        status='APPROVED',
        start_date__gte=current_month_start
    ).count()
    
    # Attendance Statistics (for today)
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='PRESENT').count()
    late_today = today_attendance.filter(status='LATE').count()
    absent_today = today_attendance.filter(status='ABSENT').count()
    
    # Recent Activities
    recent_leave_requests = LeaveRequest.objects.select_related(
        'employee', 'leave_type'
    ).order_by('-created_at')[:5]
    
    recent_employees = Employee.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]
    
    # Birthday reminders (employees with birthdays in the next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_birthdays = Employee.objects.filter(
        is_active=True,
        date_of_birth__month=today.month,
        date_of_birth__day__gte=today.day,
        date_of_birth__day__lte=next_week.day
    ) if today.month == next_week.month else Employee.objects.filter(
        Q(
            date_of_birth__month=today.month,
            date_of_birth__day__gte=today.day
        ) | Q(
            date_of_birth__month=next_week.month,
            date_of_birth__day__lte=next_week.day
        ),
        is_active=True
    )
    
    # Add dashboard data to context
    context.update({
        'hr_stats': {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'new_hires_this_month': new_hires_this_month,
            'employees_on_leave': employees_on_leave,
            'departments_with_employees': departments_with_employees,
            'pending_leave_requests': pending_leave_requests,
            'approved_leaves_this_month': approved_leaves_this_month,
            'present_today': present_today,
            'late_today': late_today,
            'absent_today': absent_today,
        },
        'recent_activities': {
            'recent_leave_requests': recent_leave_requests,
            'recent_employees': recent_employees,
            'upcoming_birthdays': upcoming_birthdays[:5],
        },
        'current_month': current_month_start.strftime('%B %Y'),
        'today': today,
    })
    
    return context


def get_admin_stats():
    """
    Helper function to get general admin statistics for the dashboard.
    """
    from hr.models import Employee, Department, Position, LeaveRequest
    
    stats = {
        'models': {
            'employees': Employee.objects.filter(is_active=True).count(),
            'departments': Department.objects.filter(is_active=True).count(),
            'positions': Position.objects.filter(is_active=True).count(),
            'pending_requests': LeaveRequest.objects.filter(status='PENDING').count(),
        }
    }
    
    return stats


def get_employee_hierarchy():
    """
    Helper function to get employee hierarchy data for organizational charts.
    """
    from hr.models import Employee
    
    # Get all managers (employees who have direct reports)
    managers = Employee.objects.filter(
        direct_reports__isnull=False,
        is_active=True
    ).distinct().select_related('department', 'position')
    
    hierarchy = []
    for manager in managers:
        direct_reports = manager.get_direct_reports()
        hierarchy.append({
            'manager': manager,
            'reports_count': direct_reports.count(),
            'direct_reports': direct_reports
        })
    
    return hierarchy


def calculate_employee_metrics(employee):
    """
    Calculate various metrics for a specific employee.
    """
    from hr.models import LeaveRequest, PerformanceReview, Attendance
    
    current_year = timezone.now().year
    
    # Leave metrics
    leave_taken = LeaveRequest.objects.filter(
        employee=employee,
        status='APPROVED',
        start_date__year=current_year
    ).aggregate(
        total_days=Count('id')
    )['total_days'] or 0
    
    # Performance metrics
    latest_review = PerformanceReview.objects.filter(
        employee=employee
    ).order_by('-review_period_end').first()
    
    # Attendance metrics for current month
    current_month = timezone.now().date().replace(day=1)
    attendance_this_month = Attendance.objects.filter(
        employee=employee,
        date__gte=current_month
    )
    
    attendance_metrics = {
        'present_days': attendance_this_month.filter(status='PRESENT').count(),
        'late_days': attendance_this_month.filter(status='LATE').count(),
        'absent_days': attendance_this_month.filter(status='ABSENT').count(),
        'total_hours': sum([
            record.hours_worked or 0 
            for record in attendance_this_month 
            if record.hours_worked
        ]),
    }
    
    return {
        'leave_taken_this_year': leave_taken,
        'latest_review': latest_review,
        'attendance_this_month': attendance_metrics,
    } 