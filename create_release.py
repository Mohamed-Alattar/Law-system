#!/usr/bin/env python3
"""
Create Release Script for Law Office Management System
This script helps prepare and create releases on GitHub
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def get_version():
    """Get version from config.py"""
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'APP_VERSION' in line and '=' in line:
                    version = line.split('=')[1].strip().strip('"').strip("'")
                    return version
        return "1.0.0"
    except:
        return "1.0.0"

def create_release_notes():
    """Create release notes"""
    version = get_version()
    date = datetime.now().strftime("%Y-%m-%d")
    
    notes = f"""# Law Office Management System v{version}
## نظام إدارة مكتب المحاماة الإصدار {version}

Released on {date}

## ✅ Features Implemented / الميزات المنفذة

### Core Modules / الوحدات الأساسية
- ✅ **User Authentication & Role Management** - نظام المصادقة وإدارة الأدوار
- ✅ **Case Management** - إدارة القضايا  
- ✅ **Client Management** - إدارة العملاء
- ✅ **Arabic Language Support** - دعم اللغة العربية
- ✅ **Database Management** - إدارة قاعدة البيانات
- ✅ **Backup & Restore** - النسخ الاحتياطي والاستعادة

### Technical Features / الميزات التقنية
- ✅ **RTL Layout Support** - دعم التخطيط من اليمين لليسار
- ✅ **Bilingual Interface** - واجهة ثنائية اللغة
- ✅ **Role-based Access Control** - التحكم في الوصول حسب الدور
- ✅ **Secure Password Hashing** - تشفير كلمات المرور الآمن
- ✅ **Modern GUI Design** - تصميم واجهة مستخدم حديث

## 🚧 Planned Features / الميزات المخططة
- Task & Appointment Management
- Document Archiving
- Billing & Accounting  
- Reports & Statistics
- AI-Powered Features

## 📋 Installation / التثبيت

### Quick Start
```bash
# Run setup script
python setup.py

# Start application  
python main.py
```

### Default Login
- Username: `admin`
- Password: `admin123`

## 🐛 Bug Fixes / إصلاح الأخطاء
- Fixed tkinter installation issue
- Improved Arabic text rendering
- Enhanced error handling
- Better installation process

## 📊 System Requirements / متطلبات النظام
- Python 3.7+
- Windows 10/11 (optimized)
- Arabic Unicode font support

## 🔗 Links / الروابط
- [Installation Guide](README.md#installation--التثبيت)
- [User Manual](README.md#usage--الاستخدام)
- [Troubleshooting](README.md#troubleshooting--استكشاف-الأخطاء)

---

**Note**: This is a demonstration version with core functionality implemented. Additional modules will be added in future releases.

**ملاحظة**: هذه نسخة تجريبية مع تنفيذ الوظائف الأساسية. سيتم إضافة وحدات إضافية في الإصدارات المستقبلية.
"""
    
    with open('RELEASE_NOTES.md', 'w', encoding='utf-8') as f:
        f.write(notes)
    
    return notes

def create_changelog():
    """Create changelog"""
    changelog = """# Changelog
All notable changes to the Law Office Management System will be documented in this file.

## [1.0.0] - 2024-01-20

### Added
- Initial release of Law Office Management System
- User authentication with role-based access control
- Case management with full CRUD operations
- Client management with relationship tracking
- Arabic language support with RTL layout
- Bilingual interface (Arabic/English)
- Database management with SQLite
- Backup and restore functionality
- Modern GUI with professional design
- Comprehensive setup and installation scripts

### Fixed
- tkinter installation issues
- Arabic text rendering problems
- Database connection handling
- Error handling and validation

### Security
- Secure password hashing with bcrypt
- SQL injection protection
- Input validation and sanitization

## [Unreleased]

### Planned
- Task and appointment management
- Document archiving system
- Billing and accounting features
- Reports and statistics
- AI-powered features
"""
    
    with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write(changelog)

def main():
    """Main function"""
    print("🏛️ Law Office Management System - Release Creator")
    print("=" * 60)
    
    version = get_version()
    print(f"Current version: {version}")
    
    # Create release notes
    print("📝 Creating release notes...")
    create_release_notes()
    
    # Create changelog
    print("📋 Creating changelog...")
    create_changelog()
    
    print("✅ Release files created:")
    print("   - RELEASE_NOTES.md")
    print("   - CHANGELOG.md")
    
    print("\n📦 To create a GitHub release:")
    print("1. Commit and push all changes:")
    print("   git add .")
    print("   git commit -m 'Prepare release v{}'".format(version))
    print("   git push")
    
    print("\n2. Create and push tag:")
    print("   git tag v{}".format(version))
    print("   git push origin v{}".format(version))
    
    print("\n3. Go to GitHub repository:")
    print("   - Click 'Releases'")
    print("   - Click 'Create a new release'")
    print("   - Select tag: v{}".format(version))
    print("   - Copy content from RELEASE_NOTES.md")
    print("   - Attach any binary files if needed")
    print("   - Click 'Publish release'")

if __name__ == "__main__":
    main()