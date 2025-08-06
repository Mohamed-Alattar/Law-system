"""
Internationalization (i18n) support for Arabic and English
"""
import os
import json
from config import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

class I18n:
    def __init__(self):
        self.current_language = DEFAULT_LANGUAGE
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation files"""
        # Arabic translations
        self.translations['ar'] = {
            # Main Menu
            'app_title': 'نظام إدارة مكتب المحاماة',
            'main_menu': 'القائمة الرئيسية',
            'dashboard': 'لوحة التحكم',
            'cases': 'القضايا',
            'clients': 'العملاء',
            'tasks': 'المهام',
            'appointments': 'المواعيد',
            'documents': 'المستندات',
            'billing': 'الفواتير',
            'reports': 'التقارير',
            'settings': 'الإعدادات',
            'logout': 'تسجيل الخروج',
            
            # Authentication
            'login': 'تسجيل الدخول',
            'username': 'اسم المستخدم',
            'password': 'كلمة المرور',
            'login_button': 'دخول',
            'login_failed': 'فشل في تسجيل الدخول',
            'invalid_credentials': 'بيانات دخول غير صحيحة',
            
            # Common terms
            'add': 'إضافة',
            'edit': 'تعديل',
            'delete': 'حذف',
            'save': 'حفظ',
            'cancel': 'إلغاء',
            'search': 'بحث',
            'view': 'عرض',
            'print': 'طباعة',
            'export': 'تصدير',
            'import': 'استيراد',
            'refresh': 'تحديث',
            'close': 'إغلاق',
            'yes': 'نعم',
            'no': 'لا',
            'ok': 'موافق',
            'confirm': 'تأكيد',
            'warning': 'تحذير',
            'error': 'خطأ',
            'success': 'نجح',
            'info': 'معلومات',
            'loading': 'جاري التحميل...',
            'please_wait': 'يرجى الانتظار...',
            
            # Case Management
            'case_management': 'إدارة القضايا',
            'add_case': 'إضافة قضية جديدة',
            'edit_case': 'تعديل القضية',
            'case_number': 'رقم القضية',
            'case_title': 'عنوان القضية',
            'client_name': 'اسم العميل',
            'court_name': 'اسم المحكمة',
            'case_type': 'نوع القضية',
            'opponent_name': 'اسم الخصم',
            'case_status': 'حالة القضية',
            'assigned_lawyer': 'المحامي المسؤول',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'description': 'الوصف',
            'open': 'مفتوح',
            'closed': 'مغلق',
            'pending': 'معلق',
            'postponed': 'مؤجل',
            
            # Client Management
            'client_management': 'إدارة العملاء',
            'add_client': 'إضافة عميل جديد',
            'edit_client': 'تعديل العميل',
            'client_name': 'اسم العميل',
            'phone': 'رقم الهاتف',
            'email': 'البريد الإلكتروني',
            'national_id': 'الرقم القومي',
            'address': 'العنوان',
            'notes': 'ملاحظات',
            
            # Task Management
            'task_management': 'إدارة المهام',
            'add_task': 'إضافة مهمة جديدة',
            'edit_task': 'تعديل المهمة',
            'task_title': 'عنوان المهمة',
            'task_description': 'وصف المهمة',
            'assigned_to': 'مُكلف إلى',
            'priority': 'الأولوية',
            'due_date': 'تاريخ الاستحقاق',
            'reminder_date': 'تاريخ التذكير',
            'task_status': 'حالة المهمة',
            'low': 'منخفض',
            'medium': 'متوسط',
            'high': 'عالي',
            'urgent': 'عاجل',
            'in_progress': 'قيد التنفيذ',
            'completed': 'مكتمل',
            'cancelled': 'ملغي',
            
            # Appointments
            'appointment_management': 'إدارة المواعيد',
            'add_appointment': 'إضافة موعد جديد',
            'edit_appointment': 'تعديل الموعد',
            'appointment_title': 'عنوان الموعد',
            'appointment_date': 'تاريخ الموعد',
            'duration': 'المدة (دقيقة)',
            'location': 'المكان',
            'attendees': 'الحضور',
            'appointment_status': 'حالة الموعد',
            'scheduled': 'مجدول',
            'rescheduled': 'معاد جدولته',
            
            # Documents
            'document_management': 'إدارة المستندات',
            'upload_document': 'رفع مستند',
            'document_title': 'عنوان المستند',
            'file_name': 'اسم الملف',
            'file_size': 'حجم الملف',
            'file_type': 'نوع الملف',
            'tags': 'العلامات',
            'uploaded_by': 'رفع بواسطة',
            'upload_date': 'تاريخ الرفع',
            
            # Billing
            'billing_management': 'إدارة الفواتير',
            'add_invoice': 'إضافة فاتورة جديدة',
            'edit_invoice': 'تعديل الفاتورة',
            'invoice_number': 'رقم الفاتورة',
            'amount': 'المبلغ',
            'tax_amount': 'مبلغ الضريبة',
            'total_amount': 'المبلغ الإجمالي',
            'issue_date': 'تاريخ الإصدار',
            'due_date': 'تاريخ الاستحقاق',
            'payment_date': 'تاريخ الدفع',
            'payment_method': 'طريقة الدفع',
            'invoice_status': 'حالة الفاتورة',
            'draft': 'مسودة',
            'sent': 'مرسل',
            'paid': 'مدفوع',
            'overdue': 'متأخر',
            
            # Reports
            'reports_statistics': 'التقارير والإحصائيات',
            'generate_report': 'توليد تقرير',
            'case_report': 'تقرير القضايا',
            'client_report': 'تقرير العملاء',
            'financial_report': 'التقرير المالي',
            'lawyer_performance': 'أداء المحامين',
            'monthly_report': 'التقرير الشهري',
            
            # Settings
            'user_management': 'إدارة المستخدمين',
            'add_user': 'إضافة مستخدم',
            'edit_user': 'تعديل المستخدم',
            'full_name': 'الاسم الكامل',
            'role': 'الدور',
            'admin': 'مدير',
            'lawyer': 'محامي',
            'secretary': 'سكرتير',
            'is_active': 'نشط',
            'backup_restore': 'النسخ الاحتياطي والاستعادة',
            'create_backup': 'إنشاء نسخة احتياطية',
            'restore_backup': 'استعادة نسخة احتياطية',
            'language': 'اللغة',
            
            # Messages
            'confirm_delete': 'هل أنت متأكد من الحذف؟',
            'delete_success': 'تم الحذف بنجاح',
            'save_success': 'تم الحفظ بنجاح',
            'update_success': 'تم التحديث بنجاح',
            'operation_failed': 'فشلت العملية',
            'no_data_found': 'لا توجد بيانات',
            'invalid_input': 'بيانات غير صحيحة',
            'required_field': 'حقل مطلوب',
            'backup_created': 'تم إنشاء النسخة الاحتياطية بنجاح',
            'backup_restored': 'تم استعادة النسخة الاحتياطية بنجاح',
        }
        
        # English translations
        self.translations['en'] = {
            # Main Menu
            'app_title': 'Law Office Management System',
            'main_menu': 'Main Menu',
            'dashboard': 'Dashboard',
            'cases': 'Cases',
            'clients': 'Clients',
            'tasks': 'Tasks',
            'appointments': 'Appointments',
            'documents': 'Documents',
            'billing': 'Billing',
            'reports': 'Reports',
            'settings': 'Settings',
            'logout': 'Logout',
            
            # Authentication
            'login': 'Login',
            'username': 'Username',
            'password': 'Password',
            'login_button': 'Login',
            'login_failed': 'Login Failed',
            'invalid_credentials': 'Invalid credentials',
            
            # Common terms
            'add': 'Add',
            'edit': 'Edit',
            'delete': 'Delete',
            'save': 'Save',
            'cancel': 'Cancel',
            'search': 'Search',
            'view': 'View',
            'print': 'Print',
            'export': 'Export',
            'import': 'Import',
            'refresh': 'Refresh',
            'close': 'Close',
            'yes': 'Yes',
            'no': 'No',
            'ok': 'OK',
            'confirm': 'Confirm',
            'warning': 'Warning',
            'error': 'Error',
            'success': 'Success',
            'info': 'Information',
            'loading': 'Loading...',
            'please_wait': 'Please wait...',
            
            # Case Management
            'case_management': 'Case Management',
            'add_case': 'Add New Case',
            'edit_case': 'Edit Case',
            'case_number': 'Case Number',
            'case_title': 'Case Title',
            'client_name': 'Client Name',
            'court_name': 'Court Name',
            'case_type': 'Case Type',
            'opponent_name': 'Opponent Name',
            'case_status': 'Case Status',
            'assigned_lawyer': 'Assigned Lawyer',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'description': 'Description',
            'open': 'Open',
            'closed': 'Closed',
            'pending': 'Pending',
            'postponed': 'Postponed',
            
            # Client Management
            'client_management': 'Client Management',
            'add_client': 'Add New Client',
            'edit_client': 'Edit Client',
            'client_name': 'Client Name',
            'phone': 'Phone',
            'email': 'Email',
            'national_id': 'National ID',
            'address': 'Address',
            'notes': 'Notes',
            
            # Task Management
            'task_management': 'Task Management',
            'add_task': 'Add New Task',
            'edit_task': 'Edit Task',
            'task_title': 'Task Title',
            'task_description': 'Task Description',
            'assigned_to': 'Assigned To',
            'priority': 'Priority',
            'due_date': 'Due Date',
            'reminder_date': 'Reminder Date',
            'task_status': 'Task Status',
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High',
            'urgent': 'Urgent',
            'in_progress': 'In Progress',
            'completed': 'Completed',
            'cancelled': 'Cancelled',
            
            # Appointments
            'appointment_management': 'Appointment Management',
            'add_appointment': 'Add New Appointment',
            'edit_appointment': 'Edit Appointment',
            'appointment_title': 'Appointment Title',
            'appointment_date': 'Appointment Date',
            'duration': 'Duration (minutes)',
            'location': 'Location',
            'attendees': 'Attendees',
            'appointment_status': 'Appointment Status',
            'scheduled': 'Scheduled',
            'rescheduled': 'Rescheduled',
            
            # Documents
            'document_management': 'Document Management',
            'upload_document': 'Upload Document',
            'document_title': 'Document Title',
            'file_name': 'File Name',
            'file_size': 'File Size',
            'file_type': 'File Type',
            'tags': 'Tags',
            'uploaded_by': 'Uploaded By',
            'upload_date': 'Upload Date',
            
            # Billing
            'billing_management': 'Billing Management',
            'add_invoice': 'Add New Invoice',
            'edit_invoice': 'Edit Invoice',
            'invoice_number': 'Invoice Number',
            'amount': 'Amount',
            'tax_amount': 'Tax Amount',
            'total_amount': 'Total Amount',
            'issue_date': 'Issue Date',
            'due_date': 'Due Date',
            'payment_date': 'Payment Date',
            'payment_method': 'Payment Method',
            'invoice_status': 'Invoice Status',
            'draft': 'Draft',
            'sent': 'Sent',
            'paid': 'Paid',
            'overdue': 'Overdue',
            
            # Reports
            'reports_statistics': 'Reports & Statistics',
            'generate_report': 'Generate Report',
            'case_report': 'Case Report',
            'client_report': 'Client Report',
            'financial_report': 'Financial Report',
            'lawyer_performance': 'Lawyer Performance',
            'monthly_report': 'Monthly Report',
            
            # Settings
            'user_management': 'User Management',
            'add_user': 'Add User',
            'edit_user': 'Edit User',
            'full_name': 'Full Name',
            'role': 'Role',
            'admin': 'Admin',
            'lawyer': 'Lawyer',
            'secretary': 'Secretary',
            'is_active': 'Active',
            'backup_restore': 'Backup & Restore',
            'create_backup': 'Create Backup',
            'restore_backup': 'Restore Backup',
            'language': 'Language',
            
            # Messages
            'confirm_delete': 'Are you sure you want to delete?',
            'delete_success': 'Deleted successfully',
            'save_success': 'Saved successfully',
            'update_success': 'Updated successfully',
            'operation_failed': 'Operation failed',
            'no_data_found': 'No data found',
            'invalid_input': 'Invalid input',
            'required_field': 'Required field',
            'backup_created': 'Backup created successfully',
            'backup_restored': 'Backup restored successfully',
        }
    
    def set_language(self, language_code):
        """Set current language"""
        if language_code in SUPPORTED_LANGUAGES:
            self.current_language = language_code
    
    def get(self, key, default=None):
        """Get translation for a key"""
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(key, default or key)
        return default or key
    
    def is_rtl(self):
        """Check if current language is right-to-left"""
        return self.current_language == 'ar'

# Global i18n instance
i18n = I18n()