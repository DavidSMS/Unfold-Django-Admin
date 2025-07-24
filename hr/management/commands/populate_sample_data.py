from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from hr.models import (
    Department, Position, Employee, LeaveType, LeaveRequest,
    PerformanceReview, Attendance
)
import random


class Command(BaseCommand):
    help = 'Populate the database with sample HR data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample HR data...')
        
        # Create Departments
        departments_data = [
            {'name': 'Human Resources', 'description': 'Manages employee relations and policies'},
            {'name': 'Engineering', 'description': 'Software development and technical operations'},
            {'name': 'Marketing', 'description': 'Brand promotion and customer acquisition'},
            {'name': 'Sales', 'description': 'Customer relations and revenue generation'},
            {'name': 'Finance', 'description': 'Financial planning and accounting'},
            {'name': 'Operations', 'description': 'Day-to-day business operations'},
        ]
        
        departments = {}
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            departments[dept.name] = dept
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        # Create Positions
        positions_data = [
            {'title': 'HR Manager', 'department': 'Human Resources', 'min_salary': 80000, 'max_salary': 120000},
            {'title': 'HR Specialist', 'department': 'Human Resources', 'min_salary': 50000, 'max_salary': 70000},
            {'title': 'Senior Software Engineer', 'department': 'Engineering', 'min_salary': 120000, 'max_salary': 180000},
            {'title': 'Software Engineer', 'department': 'Engineering', 'min_salary': 80000, 'max_salary': 120000},
            {'title': 'Junior Developer', 'department': 'Engineering', 'min_salary': 60000, 'max_salary': 80000},
            {'title': 'Marketing Manager', 'department': 'Marketing', 'min_salary': 90000, 'max_salary': 130000},
            {'title': 'Marketing Specialist', 'department': 'Marketing', 'min_salary': 55000, 'max_salary': 75000},
            {'title': 'Sales Manager', 'department': 'Sales', 'min_salary': 85000, 'max_salary': 125000},
            {'title': 'Sales Representative', 'department': 'Sales', 'min_salary': 45000, 'max_salary': 65000},
            {'title': 'Finance Manager', 'department': 'Finance', 'min_salary': 95000, 'max_salary': 140000},
            {'title': 'Accountant', 'department': 'Finance', 'min_salary': 50000, 'max_salary': 70000},
            {'title': 'Operations Manager', 'department': 'Operations', 'min_salary': 75000, 'max_salary': 110000},
        ]
        
        positions = {}
        for pos_data in positions_data:
            pos, created = Position.objects.get_or_create(
                title=pos_data['title'],
                department=departments[pos_data['department']],
                defaults={
                    'min_salary': pos_data['min_salary'],
                    'max_salary': pos_data['max_salary'],
                    'description': f'Position in {pos_data["department"]} department'
                }
            )
            positions[pos.title] = pos
            if created:
                self.stdout.write(f'Created position: {pos.title}')
        
        # Create sample employees
        employees_data = [
            {'username': 'jsmith', 'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith@company.com', 'position': 'HR Manager'},
            {'username': 'mwilson', 'first_name': 'Mary', 'last_name': 'Wilson', 'email': 'mary.wilson@company.com', 'position': 'Senior Software Engineer'},
            {'username': 'rjohnson', 'first_name': 'Robert', 'last_name': 'Johnson', 'email': 'robert.johnson@company.com', 'position': 'Marketing Manager'},
            {'username': 'sbrown', 'first_name': 'Sarah', 'last_name': 'Brown', 'email': 'sarah.brown@company.com', 'position': 'Sales Manager'},
            {'username': 'dlee', 'first_name': 'David', 'last_name': 'Lee', 'email': 'david.lee@company.com', 'position': 'Finance Manager'},
            {'username': 'ldavis', 'first_name': 'Lisa', 'last_name': 'Davis', 'email': 'lisa.davis@company.com', 'position': 'Software Engineer'},
            {'username': 'tmiller', 'first_name': 'Tom', 'last_name': 'Miller', 'email': 'tom.miller@company.com', 'position': 'Marketing Specialist'},
            {'username': 'kwilliams', 'first_name': 'Karen', 'last_name': 'Williams', 'email': 'karen.williams@company.com', 'position': 'Sales Representative'},
        ]
        
        employees = []
        for emp_data in employees_data:
            # Create or get user
            user, user_created = User.objects.get_or_create(
                username=emp_data['username'],
                defaults={
                    'first_name': emp_data['first_name'],
                    'last_name': emp_data['last_name'],
                    'email': emp_data['email'],
                    'password': 'pbkdf2_sha256$320000$test$test123'  # Default password
                }
            )
            
            # Create employee profile
            if not hasattr(user, 'employee_profile'):
                position = positions[emp_data['position']]
                employee = Employee.objects.create(
                    user=user,
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    personal_email=emp_data['email'],
                    department=position.department,
                    position=position,
                    hire_date=date.today() - timedelta(days=random.randint(30, 1000)),
                    employment_status='ACTIVE',
                    salary=random.randint(
                        int(position.min_salary) if position.min_salary else 50000,
                        int(position.max_salary) if position.max_salary else 100000
                    ),
                    date_of_birth=date(1980 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28)),
                    gender=random.choice(['M', 'F']),
                    marital_status=random.choice(['SINGLE', 'MARRIED', 'DIVORCED']),
                )
                employees.append(employee)
                self.stdout.write(f'Created employee: {employee.full_name}')
        
        # Create Leave Types
        leave_types_data = [
            {'name': 'Annual Leave', 'max_days_per_year': 25, 'is_paid': True},
            {'name': 'Sick Leave', 'max_days_per_year': 10, 'is_paid': True},
            {'name': 'Maternity Leave', 'max_days_per_year': 90, 'is_paid': True},
            {'name': 'Paternity Leave', 'max_days_per_year': 14, 'is_paid': True},
            {'name': 'Personal Leave', 'max_days_per_year': 5, 'is_paid': False},
            {'name': 'Emergency Leave', 'max_days_per_year': 3, 'is_paid': True},
        ]
        
        leave_types = []
        for leave_data in leave_types_data:
            leave_type, created = LeaveType.objects.get_or_create(
                name=leave_data['name'],
                defaults={
                    'max_days_per_year': leave_data['max_days_per_year'],
                    'is_paid': leave_data['is_paid'],
                    'description': f'{leave_data["name"]} for employees'
                }
            )
            leave_types.append(leave_type)
            if created:
                self.stdout.write(f'Created leave type: {leave_type.name}')
        
        # Create some sample leave requests
        if employees and leave_types:
            for _ in range(10):
                employee = random.choice(employees)
                leave_type = random.choice(leave_types)
                start_date = date.today() + timedelta(days=random.randint(1, 60))
                end_date = start_date + timedelta(days=random.randint(1, 5))
                
                LeaveRequest.objects.create(
                    employee=employee,
                    leave_type=leave_type,
                    start_date=start_date,
                    end_date=end_date,
                    reason=f'Sample {leave_type.name.lower()} request',
                    status=random.choice(['PENDING', 'APPROVED', 'REJECTED'])
                )
            
            self.stdout.write(f'Created 10 sample leave requests')
        
        # Create some attendance records for the past week
        if employees:
            for i in range(7):
                date_to_create = date.today() - timedelta(days=i)
                for employee in employees[:5]:  # Just for first 5 employees
                    status = random.choice(['PRESENT', 'PRESENT', 'PRESENT', 'PRESENT', 'LATE', 'ABSENT'])
                    
                    if status in ['PRESENT', 'LATE']:
                        check_in = timezone.now().replace(
                            hour=random.randint(8, 10), 
                            minute=random.randint(0, 59),
                            second=0,
                            microsecond=0
                        ).time()
                        check_out = timezone.now().replace(
                            hour=random.randint(17, 19), 
                            minute=random.randint(0, 59),
                            second=0,
                            microsecond=0
                        ).time()
                    else:
                        check_in = None
                        check_out = None
                    
                    Attendance.objects.create(
                        employee=employee,
                        date=date_to_create,
                        status=status,
                        check_in_time=check_in,
                        check_out_time=check_out,
                        break_duration=0.5 if status == 'PRESENT' else 0
                    )
            
            self.stdout.write(f'Created attendance records for past 7 days')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample HR data!')
        ) 