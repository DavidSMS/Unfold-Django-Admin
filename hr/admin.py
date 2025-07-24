from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    SingleNumericFilter,
    MultipleChoicesDropdownFilter,
)
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Department, Position, Employee, LeaveType, LeaveRequest,
    PerformanceReview, Attendance, EmployeeDocument
)


# Resources for Import/Export functionality
class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = (
            'employee_id', 'first_name', 'last_name', 'personal_email',
            'phone_number', 'department__name', 'position__title',
            'hire_date', 'employment_status', 'salary'
        )


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = ('name', 'description', 'is_active')


# Inline Admin Classes
class EmployeeDocumentInline(TabularInline):
    model = EmployeeDocument
    extra = 0
    fields = ('document_type', 'title', 'document_file', 'expiry_date', 'is_confidential')
    readonly_fields = ('upload_date',)


class PositionInline(TabularInline):
    model = Position
    extra = 0
    fields = ('title', 'description', 'min_salary', 'max_salary', 'is_active')


class DirectReportsInline(TabularInline):
    model = Employee
    fk_name = 'direct_manager'
    extra = 0
    fields = ('employee_id', 'first_name', 'last_name', 'position', 'employment_status')
    readonly_fields = ('employee_id',)
    verbose_name = "Direct Report"
    verbose_name_plural = "Direct Reports"


# Main Admin Classes
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin, ModelAdmin):
    resource_class = DepartmentResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    list_display = ('name', 'manager_link', 'employee_count_display', 'is_active', 'created_at')
    list_filter = ('is_active', ('created_at', RangeDateFilter))
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [PositionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'manager', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def manager_link(self, obj):
        if obj.manager:
            url = reverse('admin:hr_employee_change', args=[obj.manager.pk])
            return format_html('<a href="{}">{}</a>', url, obj.manager.full_name)
        return '-'
    manager_link.short_description = 'Manager'
    
    def employee_count_display(self, obj):
        return obj.employee_count
    employee_count_display.short_description = 'Active Employees'


@admin.register(Position)
class PositionAdmin(ModelAdmin):
    list_display = ('title', 'department', 'salary_range', 'is_active', 'created_at')
    list_filter = (
        'is_active',
        ('department', MultipleChoicesDropdownFilter),
        ('created_at', RangeDateFilter)
    )
    search_fields = ('title', 'description', 'department__name')
    ordering = ('title',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'department', 'description', 'requirements', 'is_active')
        }),
        ('Compensation', {
            'fields': ('min_salary', 'max_salary'),
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def salary_range(self, obj):
        if obj.min_salary and obj.max_salary:
            return f"${obj.min_salary:,.0f} - ${obj.max_salary:,.0f}"
        elif obj.min_salary:
            return f"${obj.min_salary:,.0f}+"
        return '-'
    salary_range.short_description = 'Salary Range'


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin, ModelAdmin):
    resource_class = EmployeeResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    list_display = (
        'employee_photo_thumbnail', 'employee_id', 'full_name', 'department',
        'position', 'employment_status', 'hire_date', 'years_of_service_display'
    )
    list_filter = (
        ('employment_status', MultipleChoicesDropdownFilter),
        ('department', MultipleChoicesDropdownFilter),
        ('gender', MultipleChoicesDropdownFilter),
        ('hire_date', RangeDateFilter),
        'is_active'
    )
    search_fields = (
        'employee_id', 'first_name', 'last_name', 'personal_email',
        'user__email', 'user__username'
    )
    ordering = ('last_name', 'first_name')
    inlines = [DirectReportsInline, EmployeeDocumentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'user', 'employee_photo')
        }),
        ('Personal Information', {
            'fields': (
                ('first_name', 'middle_name', 'last_name'),
                ('date_of_birth', 'gender', 'marital_status'),
                'nationality'
            )
        }),
        ('Contact Information', {
            'fields': (
                ('personal_email', 'phone_number'),
                ('emergency_contact_name', 'emergency_contact_phone'),
                'emergency_contact_relationship'
            )
        }),
        ('Address', {
            'fields': (
                ('address_line1', 'address_line2'),
                ('city', 'state', 'postal_code'),
                'country'
            ),
            'classes': ('collapse',)
        }),
        ('Employment Information', {
            'fields': (
                ('department', 'position'),
                'direct_manager',
                ('hire_date', 'employment_status'),
                ('termination_date', 'termination_reason')
            )
        }),
        ('Compensation', {
            'fields': (('salary', 'salary_currency'),),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('is_active', 'notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('employee_id', 'created_at', 'updated_at')
    
    def employee_photo_thumbnail(self, obj):
        if obj.employee_photo:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%;" />',
                obj.employee_photo.url
            )
        return format_html(
            '<div style="width: 40px; height: 40px; background: #e0e0e0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px;">No Photo</div>'
        )
    employee_photo_thumbnail.short_description = 'Photo'
    
    def years_of_service_display(self, obj):
        years = obj.years_of_service
        if years == 1:
            return "1 year"
        return f"{years} years"
    years_of_service_display.short_description = 'Service'


@admin.register(LeaveType)
class LeaveTypeAdmin(ModelAdmin):
    list_display = ('name', 'max_days_per_year', 'is_paid', 'requires_approval', 'is_active')
    list_filter = ('is_paid', 'requires_approval', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'max_days_per_year')
        }),
        ('Settings', {
            'fields': ('is_paid', 'requires_approval', 'is_active')
        }),
    )


@admin.register(LeaveRequest)
class LeaveRequestAdmin(ModelAdmin):
    list_display = (
        'employee', 'leave_type', 'start_date', 'end_date',
        'duration_days_display', 'status', 'created_at'
    )
    list_filter = (
        ('status', MultipleChoicesDropdownFilter),
        ('leave_type', MultipleChoicesDropdownFilter),
        ('start_date', RangeDateFilter),
        ('created_at', RangeDateFilter)
    )
    search_fields = ('employee__first_name', 'employee__last_name', 'reason')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Leave Information', {
            'fields': ('employee', 'leave_type', ('start_date', 'end_date'), 'reason')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'approval_date', 'rejection_reason')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def duration_days_display(self, obj):
        return f"{obj.duration_days} days"
    duration_days_display.short_description = 'Duration'


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(ModelAdmin):
    list_display = (
        'employee', 'reviewer', 'review_type', 'review_period_end',
        'overall_rating', 'average_rating_display', 'is_final'
    )
    list_filter = (
        ('review_type', MultipleChoicesDropdownFilter),
        ('overall_rating', SingleNumericFilter),
        ('review_period_end', RangeDateFilter),
        'is_final'
    )
    search_fields = ('employee__first_name', 'employee__last_name', 'reviewer__first_name')
    ordering = ('-review_period_end',)
    
    fieldsets = (
        ('Review Information', {
            'fields': (
                ('employee', 'reviewer'),
                ('review_period_start', 'review_period_end'),
                'review_type'
            )
        }),
        ('Performance Ratings', {
            'fields': (
                ('overall_rating', 'goals_achievement'),
                ('quality_of_work', 'communication'),
                ('teamwork', 'leadership')
            )
        }),
        ('Comments', {
            'fields': (
                'strengths',
                'areas_for_improvement',
                'goals_for_next_period',
                'employee_comments',
                'additional_notes'
            )
        }),
        ('Status', {
            'fields': ('is_final',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def average_rating_display(self, obj):
        return f"{obj.average_rating:.1f}"
    average_rating_display.short_description = 'Avg Rating'


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = (
        'employee', 'date', 'status', 'check_in_time',
        'check_out_time', 'hours_worked', 'overtime_hours'
    )
    list_filter = (
        ('status', MultipleChoicesDropdownFilter),
        ('date', RangeDateFilter),
        ('hours_worked', SingleNumericFilter)
    )
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('-date',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('employee', 'date', 'status')
        }),
        ('Time Information', {
            'fields': (
                ('check_in_time', 'check_out_time'),
                ('hours_worked', 'overtime_hours'),
                'break_duration'
            )
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(ModelAdmin):
    list_display = (
        'employee', 'document_type', 'title', 'upload_date',
        'expiry_date', 'is_confidential'
    )
    list_filter = (
        ('document_type', MultipleChoicesDropdownFilter),
        ('upload_date', RangeDateFilter),
        ('expiry_date', RangeDateFilter),
        'is_confidential'
    )
    search_fields = ('employee__first_name', 'employee__last_name', 'title')
    ordering = ('-upload_date',)
    
    fieldsets = (
        ('Document Information', {
            'fields': ('employee', 'document_type', 'title', 'description')
        }),
        ('File Information', {
            'fields': ('document_file', 'expiry_date', 'is_confidential')
        }),
        ('System Information', {
            'fields': ('upload_date', 'uploaded_by'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('upload_date', 'uploaded_by')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set on creation
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


# Extend User Admin to show employee profile link
class EmployeeInline(StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee Profile'
    fields = (
        ('first_name', 'last_name'),
        ('department', 'position'),
        'employee_photo'
    )


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
