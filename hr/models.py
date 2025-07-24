from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import date, datetime
import uuid


class Department(models.Model):
    """Department model for organizing employees"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(
        'Employee', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_department'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    @property
    def employee_count(self):
        return self.employees.filter(is_active=True).count()


class Position(models.Model):
    """Job position/title model"""
    title = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='positions'
    )
    description = models.TextField(blank=True)
    min_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    max_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    requirements = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'department']
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.title} - {self.department.name}"


class Employee(models.Model):
    """Employee model with comprehensive information"""
    
    EMPLOYMENT_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('TERMINATED', 'Terminated'),
        ('ON_LEAVE', 'On Leave'),
        ('PROBATION', 'Probation'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated'),
    ]

    # Basic Information
    employee_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='employee_profile'
    )
    
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    marital_status = models.CharField(
        max_length=10, 
        choices=MARITAL_STATUS_CHOICES, 
        blank=True
    )
    nationality = models.CharField(max_length=50, blank=True)
    
    # Contact Information
    personal_email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = PhoneNumberField(blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Employment Information
    employee_photo = models.ImageField(
        upload_to='employee_photos/', 
        blank=True, 
        null=True
    )
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='employees'
    )
    position = models.ForeignKey(
        Position, 
        on_delete=models.SET_NULL, 
        null=True
    )
    direct_manager = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='direct_reports'
    )
    hire_date = models.DateField(default=date.today)
    employment_status = models.CharField(
        max_length=15, 
        choices=EMPLOYMENT_STATUS_CHOICES, 
        default='ACTIVE'
    )
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(blank=True)
    
    # Compensation Information
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    salary_currency = models.CharField(max_length=3, default='USD')
    
    # System Information
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Generate employee ID
            self.employee_id = f"EMP{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < 
                (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    @property
    def years_of_service(self):
        if self.hire_date:
            today = date.today()
            return today.year - self.hire_date.year - (
                (today.month, today.day) < 
                (self.hire_date.month, self.hire_date.day)
            )
        return 0

    def get_direct_reports(self):
        return Employee.objects.filter(direct_manager=self, is_active=True)


class LeaveType(models.Model):
    """Leave type model for different types of leave"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    max_days_per_year = models.PositiveIntegerField(null=True, blank=True)
    is_paid = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    """Leave request model for employee leave applications"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='leave_requests'
    )
    leave_type = models.ForeignKey(
        LeaveType, 
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )
    approved_by = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_leaves'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.name} ({self.start_date} to {self.end_date})"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("Start date cannot be after end date.")


class PerformanceReview(models.Model):
    """Performance review model for employee evaluations"""
    
    REVIEW_TYPE_CHOICES = [
        ('ANNUAL', 'Annual Review'),
        ('QUARTERLY', 'Quarterly Review'),
        ('PROBATION', 'Probation Review'),
        ('PROJECT', 'Project Review'),
        ('360', '360 Degree Review'),
    ]
    
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Below Average'),
        (3, 'Average'),
        (4, 'Above Average'),
        (5, 'Excellent'),
    ]

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='performance_reviews'
    )
    reviewer = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='conducted_reviews'
    )
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    review_type = models.CharField(
        max_length=15, 
        choices=REVIEW_TYPE_CHOICES, 
        default='ANNUAL'
    )
    
    # Performance Areas
    overall_rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    goals_achievement = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    quality_of_work = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    teamwork = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    leadership = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, 
        blank=True
    )
    
    # Comments
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    goals_for_next_period = models.TextField()
    employee_comments = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    
    # Review Status
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-review_period_end']
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'

    def __str__(self):
        return f"{self.employee.full_name} - {self.review_type} ({self.review_period_start} to {self.review_period_end})"

    @property
    def average_rating(self):
        ratings = [
            self.overall_rating,
            self.goals_achievement,
            self.quality_of_work,
            self.communication,
            self.teamwork,
        ]
        if self.leadership:
            ratings.append(self.leadership)
        return sum(ratings) / len(ratings)


class Attendance(models.Model):
    """Attendance model for tracking employee work hours"""
    
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('HALF_DAY', 'Half Day'),
        ('WORK_FROM_HOME', 'Work from Home'),
        ('ON_LEAVE', 'On Leave'),
        ('HOLIDAY', 'Holiday'),
    ]

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='attendance_records'
    )
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='PRESENT'
    )
    hours_worked = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    overtime_hours = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=0
    )
    break_duration = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=0,
        help_text="Break duration in hours"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.status})"

    def save(self, *args, **kwargs):
        # Calculate hours worked if check in and check out times are provided
        if self.check_in_time and self.check_out_time:
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            
            # Handle overnight shifts
            if check_out < check_in:
                check_out += timezone.timedelta(days=1)
            
            duration = check_out - check_in
            total_hours = duration.total_seconds() / 3600
            
            # Subtract break duration
            self.hours_worked = total_hours - float(self.break_duration)
            
            # Calculate overtime (assuming 8 hours is standard)
            if self.hours_worked > 8:
                self.overtime_hours = self.hours_worked - 8
            else:
                self.overtime_hours = 0
                
        super().save(*args, **kwargs)


class EmployeeDocument(models.Model):
    """Model for storing employee documents"""
    
    DOCUMENT_TYPE_CHOICES = [
        ('CONTRACT', 'Employment Contract'),
        ('ID_COPY', 'ID Copy'),
        ('RESUME', 'Resume/CV'),
        ('CERTIFICATE', 'Certificate'),
        ('REFERENCE', 'Reference Letter'),
        ('MEDICAL', 'Medical Certificate'),
        ('OTHER', 'Other'),
    ]

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=15, 
        choices=DOCUMENT_TYPE_CHOICES
    )
    title = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='employee_documents/')
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True
    )
    expiry_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)

    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Employee Document'
        verbose_name_plural = 'Employee Documents'

    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"
