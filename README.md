# Law Office Management System
## نظام إدارة مكتب المحاماة

A comprehensive law office management system designed specifically for Egyptian law firms, with full Arabic and English language support and right-to-left (RTL) layout for Arabic text.

## Features / الميزات

### ✅ Core Features (Implemented)
- **User Authentication & Role Management** - نظام المصادقة وإدارة الأدوار
  - Secure login system with password hashing
  - Role-based access control (Admin, Lawyer, Secretary)
  - Default admin account: `admin` / `admin123`

- **Case Management** - إدارة القضايا
  - Add, edit, and delete legal cases
  - Case details: number, title, client, court, type, status, assigned lawyer
  - Search and filter capabilities
  - Case status tracking (Open, Closed, Pending, Postponed)

- **Client Management** - إدارة العملاء
  - Complete client records with contact information
  - National ID management
  - Client case history view
  - Search and filtering

- **Arabic Language Support** - دعم اللغة العربية
  - Full Arabic interface with RTL layout
  - Bilingual support (Arabic/English)
  - Proper Arabic text rendering and display

- **Database Management** - إدارة قاعدة البيانات
  - Local SQLite database for offline access
  - Backup and restore functionality
  - Data integrity and security

### 🚧 Coming Soon Features
- **Task & Appointment Management** - إدارة المهام والمواعيد
- **Document Archiving** - أرشفة المستندات  
- **Billing & Accounting** - الفواتير والمحاسبة
- **Reports & Statistics** - التقارير والإحصائيات
- **AI-Powered Features** - الميزات المدعومة بالذكاء الاصطناعي

## Installation / التثبيت

### Prerequisites / المتطلبات
- Python 3.7 or higher
- Windows 10/11 (optimized for Windows)

### Step 1: Run Setup Script (Recommended)
```bash
python setup.py
```
This will automatically:
- Check Python version compatibility
- Verify tkinter availability
- Install all required dependencies
- Create necessary directories
- Test Arabic text rendering
- Run a GUI test

### Step 2: Manual Installation (Alternative)
If you prefer manual installation:
```bash
pip install -r requirements.txt
```

Required packages:
- `tkinter` (built into Python - no installation needed)
- `Pillow==10.1.0`
- `reportlab==4.0.7`
- `openpyxl==3.1.2`
- `python-dateutil==2.8.2`
- `cryptography==41.0.8`
- `bcrypt==4.1.2`
- `tkcalendar==1.6.1`
- `babel==2.13.1`
- `arabic-reshaper==3.0.0`
- `python-bidi==0.4.2`

### Step 3: Run the Application
```bash
python main.py
```
Or on Windows, double-click `run_law_office.bat`

## Usage / الاستخدام

### First Time Setup
1. **Recommended**: Run the setup script first:
   ```bash
   python setup.py
   ```
2. Or use the comprehensive Windows launcher: `setup_and_run.bat`
3. For quick testing, run: `python test_installation.py`
4. Start the application: `python main.py`
5. Use default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
6. Change language using the dropdown in login screen
7. Create additional users through Settings > User Management (Admin only)

### Navigation / التنقل
- **Dashboard**: Overview with statistics and recent activities
- **Cases**: Manage legal cases
- **Clients**: Manage client information
- **Tasks**: Task and deadline management (Coming Soon)
- **Appointments**: Calendar and appointment scheduling (Coming Soon)
- **Documents**: Document archiving system (Coming Soon)
- **Billing**: Invoice and payment management (Coming Soon)
- **Reports**: Generate various reports (Coming Soon)

### User Roles / أدوار المستخدمين

#### Admin (مدير)
- Full system access
- User management
- System settings
- All modules access

#### Lawyer (محامي)
- Case management
- Client management
- Financial reports access
- Document management

#### Secretary (سكرتير)
- Basic case viewing
- Client management
- Appointment scheduling
- Limited access

## File Structure / هيكل الملفات

```
law_office_management/
├── main.py                    # Main application entry point
├── setup.py                   # Setup and installation script
├── test_installation.py       # Installation verification script
├── config.py                  # Configuration settings
├── database.py                # Database models and management
├── auth.py                    # Authentication and user management
├── i18n.py                    # Internationalization (Arabic/English)
├── gui_components.py          # Reusable GUI components with RTL support
├── login_window.py            # Login interface
├── main_window.py             # Main application window
├── case_management.py         # Case management module
├── client_management.py       # Client management module
├── task_management.py         # Task management (placeholder)
├── appointment_management.py  # Appointment management (placeholder)
├── document_management.py     # Document management (placeholder)
├── billing_management.py      # Billing management (placeholder)
├── reports.py                 # Reports module (placeholder)
├── user_management_ui.py      # User management interface (placeholder)
├── requirements.txt           # Python dependencies (no tkinter)
├── run_law_office.bat         # Simple Windows launcher
├── setup_and_run.bat          # Complete Windows setup and launcher
├── README.md                  # This file
└── data/                      # Application data directory (auto-created)
    ├── law_office.db          # SQLite database (auto-created)
    ├── documents/             # Document storage
    ├── backups/               # Database backups
    └── reports/               # Generated reports
```

## Database Schema / مخطط قاعدة البيانات

### Tables / الجداول
- **users** - System users with roles
- **clients** - Client information
- **cases** - Legal cases
- **tasks** - Tasks and deadlines
- **appointments** - Appointments and calendar events
- **documents** - Document metadata
- **invoices** - Billing and invoices
- **case_sessions** - Court sessions and hearings
- **settings** - Application settings

## Technical Features / الميزات التقنية

### Arabic Language Support
- **RTL Layout**: Proper right-to-left layout for Arabic interface
- **Text Shaping**: Arabic text reshaping using `arabic-reshaper`
- **BiDi Algorithm**: Bidirectional text rendering using `python-bidi`
- **Font Support**: Arabic Unicode font support

### Security
- **Password Hashing**: Using bcrypt for secure password storage
- **Role-Based Access**: Different permission levels
- **Session Management**: Secure user session handling

### Data Management
- **SQLite Database**: Lightweight, serverless database
- **Backup/Restore**: Built-in database backup and restore
- **Data Validation**: Input validation and error handling

## Customization / التخصيص

### Adding New Languages
1. Edit `i18n.py` and add translations to the `translations` dictionary
2. Add language code to `SUPPORTED_LANGUAGES` in `config.py`
3. Update language selection UI components

### Modifying Colors and Styling
Edit the color constants in `config.py`:
- `PRIMARY_COLOR`
- `SECONDARY_COLOR`
- `SUCCESS_COLOR`
- `WARNING_COLOR`
- `DANGER_COLOR`
- `BACKGROUND_COLOR`

### Database Modifications
1. Update schema in `database.py`
2. Add migration logic for existing databases
3. Update corresponding UI modules

## Troubleshooting / استكشاف الأخطاء

### Common Issues

#### "Missing Dependencies" Error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### "Could not find a version that satisfies the requirement tkinter" Error
This error occurs because `tkinter` is built into Python and should not be installed via pip. 

**Solution:**
1. Remove `tkinter` from requirements.txt (already done in latest version)
2. Run the setup script: `python setup.py`
3. If tkinter is still missing, you may need to install it system-wide:
   - **Windows**: Reinstall Python with tkinter enabled
   - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
   - **CentOS/RHEL**: `sudo yum install tkinter`
   - **macOS**: `brew install python-tk`

#### Arabic Text Not Displaying Correctly
Ensure you have Arabic Unicode fonts installed on your system:
- Windows: Arial Unicode MS (usually pre-installed)
- Fallback: Install additional Arabic fonts

#### Database Connection Issues
- Check if `data/` directory exists and is writable
- Verify SQLite installation
- Check file permissions

#### Application Won't Start
1. Verify Python version (3.7+)
2. Check all dependencies are installed
3. Run from command line to see error messages

### Log Files
Check the console output for error messages when running:
```bash
python main.py
```

## Contributing / المساهمة

This is a demo application. For production use, consider:

### Security Enhancements
- Implement additional authentication methods
- Add audit logging
- Enhance data encryption

### Feature Completions
- Complete remaining modules (Tasks, Documents, Billing, Reports)
- Add AI-powered features
- Implement advanced search capabilities

### Performance Optimizations
- Add database indexing
- Implement caching mechanisms
- Optimize large data handling

## License / الترخيص

This project is provided as-is for educational and demonstration purposes.

## Support / الدعم

For issues and questions:
1. Check the troubleshooting section above
2. Review error messages in console output
3. Verify system requirements and dependencies

---

**Note**: This is a demonstration version with core case and client management features implemented. Additional modules are planned for future development.

**ملاحظة**: هذه نسخة تجريبية مع تنفيذ الميزات الأساسية لإدارة القضايا والعملاء. الوحدات الإضافية مخططة للتطوير المستقبلي.