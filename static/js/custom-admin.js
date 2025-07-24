// Custom JavaScript for HR Management System Admin

document.addEventListener('DOMContentLoaded', function() {
    
    // Employee photo preview functionality
    function setupPhotoPreview() {
        const photoInputs = document.querySelectorAll('input[type="file"][name$="employee_photo"]');
        
        photoInputs.forEach(function(input) {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        // Create or update preview image
                        let preview = document.querySelector('.employee-photo-preview');
                        if (!preview) {
                            preview = document.createElement('img');
                            preview.className = 'employee-photo-preview';
                            preview.style.marginTop = '10px';
                            input.parentNode.appendChild(preview);
                        }
                        preview.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            });
        });
    }
    
    // Auto-calculate hours worked
    function setupTimeCalculation() {
        const checkInInputs = document.querySelectorAll('input[name$="check_in_time"]');
        const checkOutInputs = document.querySelectorAll('input[name$="check_out_time"]');
        
        function calculateHours(checkInInput, checkOutInput) {
            const checkIn = checkInInput.value;
            const checkOut = checkOutInput.value;
            
            if (checkIn && checkOut) {
                const checkInTime = new Date('1970-01-01 ' + checkIn);
                const checkOutTime = new Date('1970-01-01 ' + checkOut);
                
                // Handle overnight shifts
                if (checkOutTime < checkInTime) {
                    checkOutTime.setDate(checkOutTime.getDate() + 1);
                }
                
                const diffMs = checkOutTime - checkInTime;
                const diffHours = diffMs / (1000 * 60 * 60);
                
                // Find and update hours worked field
                const hoursWorkedInput = document.querySelector('input[name$="hours_worked"]');
                if (hoursWorkedInput) {
                    hoursWorkedInput.value = diffHours.toFixed(2);
                }
            }
        }
        
        checkInInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                const checkOutInput = document.querySelector('input[name$="check_out_time"]');
                if (checkOutInput) {
                    calculateHours(input, checkOutInput);
                }
            });
        });
        
        checkOutInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                const checkInInput = document.querySelector('input[name$="check_in_time"]');
                if (checkInInput) {
                    calculateHours(checkInInput, input);
                }
            });
        });
    }
    
    // Salary formatting
    function setupSalaryFormatting() {
        const salaryInputs = document.querySelectorAll('input[name$="salary"], input[name$="min_salary"], input[name$="max_salary"]');
        
        salaryInputs.forEach(function(input) {
            input.addEventListener('blur', function() {
                const value = parseFloat(this.value);
                if (!isNaN(value)) {
                    this.value = value.toFixed(2);
                }
            });
        });
    }
    
    // Quick actions for employee management
    function setupQuickActions() {
        // Add quick action buttons to employee list
        const employeeRows = document.querySelectorAll('.admin-object-tools-list li');
        
        if (employeeRows.length > 0 && window.location.pathname.includes('/hr/employee/')) {
            // Add custom actions
            const quickActionsDiv = document.createElement('div');
            quickActionsDiv.className = 'hr-quick-actions';
            quickActionsDiv.innerHTML = `
                <a href="#" class="hr-quick-action-btn" onclick="generateReport()">Generate Report</a>
                <a href="#" class="hr-quick-action-btn" onclick="exportData()">Export Data</a>
            `;
            
            const breadcrumbs = document.querySelector('.breadcrumbs');
            if (breadcrumbs) {
                breadcrumbs.parentNode.insertBefore(quickActionsDiv, breadcrumbs.nextSibling);
            }
        }
    }
    
    // Dashboard statistics refresh
    function setupDashboardRefresh() {
        if (window.location.pathname === '/admin/') {
            // Add refresh button for dashboard stats
            setInterval(function() {
                // Auto-refresh dashboard every 5 minutes
                if (document.hidden === false) {
                    location.reload();
                }
            }, 300000); // 5 minutes
        }
    }
    
    // Form validation enhancements
    function setupFormValidation() {
        // Date validation for employee forms
        const hireDateInputs = document.querySelectorAll('input[name$="hire_date"]');
        const birthDateInputs = document.querySelectorAll('input[name$="date_of_birth"]');
        
        hireDateInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                const hireDate = new Date(this.value);
                const today = new Date();
                
                if (hireDate > today) {
                    alert('Hire date cannot be in the future.');
                    this.value = '';
                }
            });
        });
        
        birthDateInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                const birthDate = new Date(this.value);
                const today = new Date();
                const age = today.getFullYear() - birthDate.getFullYear();
                
                if (age < 16 || age > 100) {
                    alert('Please enter a valid birth date.');
                    this.value = '';
                }
            });
        });
        
        // Leave request date validation
        const leaveStartInputs = document.querySelectorAll('input[name$="start_date"]');
        const leaveEndInputs = document.querySelectorAll('input[name$="end_date"]');
        
        function validateLeaveDates() {
            leaveStartInputs.forEach(function(startInput) {
                const endInput = document.querySelector('input[name$="end_date"]');
                if (startInput.value && endInput && endInput.value) {
                    const startDate = new Date(startInput.value);
                    const endDate = new Date(endInput.value);
                    
                    if (startDate > endDate) {
                        alert('Start date cannot be after end date.');
                        startInput.value = '';
                        endInput.value = '';
                    }
                }
            });
        }
        
        leaveStartInputs.forEach(function(input) {
            input.addEventListener('change', validateLeaveDates);
        });
        
        leaveEndInputs.forEach(function(input) {
            input.addEventListener('change', validateLeaveDates);
        });
    }
    
    // Initialize all features
    setupPhotoPreview();
    setupTimeCalculation();
    setupSalaryFormatting();
    setupQuickActions();
    setupDashboardRefresh();
    setupFormValidation();
    
    // Add loading states for form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitButtons = form.querySelectorAll('input[type="submit"], button[type="submit"]');
            submitButtons.forEach(function(button) {
                button.disabled = true;
                button.classList.add('hr-loading');
                button.value = button.value + ' (Processing...)';
            });
        });
    });
});

// Global functions for quick actions
function generateReport() {
    alert('Report generation feature will be implemented in a future update.');
}

function exportData() {
    alert('Data export feature will be implemented in a future update.');
}

// Utility function for AJAX requests
function makeAjaxRequest(url, method, data, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    // Add CSRF token if available
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken.value);
    }
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                if (callback) callback(JSON.parse(xhr.responseText));
            } else {
                console.error('AJAX request failed:', xhr.status);
            }
        }
    };
    
    xhr.send(JSON.stringify(data));
} 