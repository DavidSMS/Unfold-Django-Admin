# HR Management System

A comprehensive Human Resources Management System built with Django and enhanced with django-unfold for a modern admin interface.

## Features

### 🏢 Core HR Functionality
- **Employee Management**: Complete employee profiles with personal, contact, and employment information
- **Department & Position Management**: Organize employees by departments and job positions
- **Leave Management**: Handle various types of leave requests with approval workflows
- **Performance Reviews**: Conduct and track employee performance evaluations
- **Attendance Tracking**: Monitor employee attendance with check-in/check-out times
- **Document Management**: Store and manage employee documents securely

### 🎨 Modern Admin Interface
- **Django Unfold Integration**: Beautiful, modern admin interface with responsive design
- **Custom Dashboard**: HR-specific dashboard with statistics and quick insights
- **Advanced Filtering**: Powerful filtering options for all HR data
- **Import/Export**: Bulk import and export functionality for employee data
- **Real-time Statistics**: Live dashboard with employee metrics and trends

## Screenshots

The admin interface features:
- Modern, clean design with dark/light mode support
- Responsive layout that works on all devices
- Custom navigation with HR-specific sections
- Advanced filtering and search capabilities
- Rich dashboard with statistics and quick actions

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository** (if applicable) or use the provided files:
   ```bash
   cd Unfold-Admin
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate with sample data** (optional):
   ```bash
   python manage.py populate_sample_data
   ```

8. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the admin interface**:
   Open your browser and go to `http://127.0.0.1:8000/admin/`

### Default Credentials

If you used the sample data command, you can use these credentials:
- **Username**: admin
- **Password**: admin123

## Configuration

### Environment Variables

The application uses environment variables for configuration. Key variables include:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=UTC
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Django Unfold Customization

The admin interface is customized through the `UNFOLD` setting in `settings.py`. Key customizations include:
- Custom branding and colors
- HR-specific navigation
- Dashboard widgets
- Custom styling

## Usage

### Employee Management

1. **Adding Employees**:
   - Go to HR → Employees → Add Employee
   - Fill in personal, contact, and employment information
   - Upload employee photo (optional)
   - Assign to department and position

2. **Managing Departments**:
   - Create departments with descriptions
   - Assign managers to departments
   - View employee counts per department

3. **Position Management**:
   - Define job positions with salary ranges
   - Link positions to departments
   - Set requirements and descriptions

### Leave Management

1. **Leave Types**:
   - Configure different types of leave (Annual, Sick, Maternity, etc.)
   - Set maximum days per year
   - Define if leave is paid or unpaid

2. **Leave Requests**:
   - Employees can request leave through the system
   - Managers can approve or reject requests
   - Track leave balances and history

### Performance Reviews

1. **Review Process**:
   - Create performance reviews for employees
   - Rate performance across multiple criteria
   - Add detailed comments and improvement areas
   - Set goals for next review period

### Attendance Tracking

1. **Daily Attendance**:
   - Record check-in and check-out times
   - Track breaks and overtime
   - Monitor attendance patterns
   - Generate attendance reports

## Project Structure

```
hr_system/
├── hr/                     # Main HR application
│   ├── models.py          # Database models
│   ├── admin.py           # Admin interface configuration
│   ├── management/        # Management commands
│   └── migrations/        # Database migrations
├── hr_system/             # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # URL configuration
│   └── utils.py          # Utility functions
├── static/                # Static files (CSS, JS)
├── media/                 # File uploads
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## Key Models

### Employee
- Personal information (name, DOB, contact details)
- Employment information (department, position, salary)
- Relationships (manager, direct reports)
- Documents and photos

### Department
- Basic information and description
- Manager assignment
- Employee count tracking

### Position
- Job titles and descriptions
- Salary ranges
- Department relationships

### Leave Request
- Employee and leave type
- Date ranges and duration
- Approval workflow
- Status tracking

### Performance Review
- Multi-criteria rating system
- Comments and feedback
- Goal setting
- Review history

### Attendance
- Daily attendance records
- Time tracking
- Status monitoring
- Overtime calculation

## Advanced Features

### Import/Export
- Bulk import employees via CSV/Excel
- Export reports in multiple formats
- Data validation and error handling

### Dashboard Analytics
- Employee statistics
- Attendance summaries
- Leave request metrics
- Performance insights

### Security Features
- User authentication and authorization
- Document access controls
- Audit logging
- Data encryption for sensitive information

## Customization

### Adding Custom Fields

To add custom fields to models:

1. Edit the model in `hr/models.py`
2. Create and run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Update admin configuration in `hr/admin.py`

### Custom Admin Views

The admin interface can be customized by:
- Modifying `UNFOLD` settings in `settings.py`
- Adding custom CSS in `static/css/custom-admin.css`
- Extending JavaScript functionality in `static/js/custom-admin.js`

### Custom Reports

Add custom management commands in `hr/management/commands/` for:
- Generating reports
- Data analysis
- Automated tasks

## Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

The project follows Django best practices:
- Proper model relationships
- Admin interface customization
- Environment-based configuration
- Comprehensive documentation

### Contributing

1. Follow Django coding standards
2. Add tests for new features
3. Update documentation
4. Ensure compatibility with django-unfold

## Deployment

### Production Considerations

1. **Security**:
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure proper `ALLOWED_HOSTS`
   - Use HTTPS

2. **Database**:
   - Use PostgreSQL or MySQL for production
   - Set up regular backups
   - Configure connection pooling

3. **Static Files**:
   - Configure static file serving
   - Use CDN for media files
   - Enable compression

4. **Monitoring**:
   - Set up logging
   - Monitor performance
   - Configure error tracking

### Environment Setup

For production deployment:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Configure reverse proxy (Nginx, Apache)
3. Set up SSL certificates
4. Configure database backups
5. Implement monitoring and logging

## Technology Stack

- **Backend**: Django 4.2+
- **Admin Interface**: django-unfold
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Frontend**: HTML5, CSS3, JavaScript (admin interface)
- **File Storage**: Local filesystem (configurable)
- **Authentication**: Django built-in auth system

## License

This project is built using open-source technologies and follows best practices for HR management systems.

## Support

For issues and questions:
1. Check the Django documentation
2. Review django-unfold documentation
3. Check the admin interface logs
4. Verify environment configuration

## Changelog

### v1.0.0
- Initial release with core HR functionality
- Django Unfold integration
- Employee management system
- Leave management
- Performance reviews
- Attendance tracking
- Document management
- Sample data population
- Comprehensive admin interface 