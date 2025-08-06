#!/usr/bin/env python3
"""
Setup script for Law Office Management System
This script helps install dependencies and check system requirements
"""

import sys
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        print("✅ tkinter is available")
        return True
    except ImportError:
        print("❌ tkinter is not available")
        print("   On Ubuntu/Debian: sudo apt-get install python3-tk")
        print("   On CentOS/RHEL: sudo yum install tkinter")
        print("   On Windows: tkinter should be included with Python")
        return False

def install_dependencies():
    """Install required dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt file not found")
        return False

def test_arabic_support():
    """Test Arabic text rendering"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        # Test Arabic text
        test_text = "مرحبا بكم في نظام إدارة مكتب المحاماة"
        reshaped_text = arabic_reshaper.reshape(test_text)
        bidi_text = get_display(reshaped_text)
        
        print("✅ Arabic text rendering is working")
        return True
    except Exception as e:
        print(f"❌ Arabic text rendering error: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    import os
    
    directories = ['data', 'data/documents', 'data/backups', 'data/reports']
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Error creating directory {directory}: {e}")
            return False
    
    return True

def test_database():
    """Test database creation"""
    try:
        import sqlite3
        import os
        
        # Test database creation
        test_db = os.path.join('data', 'test.db')
        conn = sqlite3.connect(test_db)
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        conn.close()
        
        # Clean up
        if os.path.exists(test_db):
            os.remove(test_db)
        
        print("✅ Database functionality is working")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def show_gui_test():
    """Show a simple GUI test"""
    try:
        root = tk.Tk()
        root.title("Law Office Management System - Setup Test")
        root.geometry("400x200")
        
        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (200)
        y = (root.winfo_screenheight() // 2) - (100)
        root.geometry(f"400x200+{x}+{y}")
        
        # Test Arabic text
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            test_text = "نظام إدارة مكتب المحاماة"
            reshaped_text = arabic_reshaper.reshape(test_text)
            bidi_text = get_display(reshaped_text)
            arabic_label = tk.Label(root, text=bidi_text, font=("Arial Unicode MS", 14))
            arabic_label.pack(pady=10)
        except:
            pass
        
        english_label = tk.Label(root, text="Law Office Management System", font=("Arial", 14, "bold"))
        english_label.pack(pady=5)
        
        status_label = tk.Label(root, text="✅ Setup completed successfully!", fg="green", font=("Arial", 12))
        status_label.pack(pady=10)
        
        close_button = tk.Button(root, text="Close", command=root.destroy, bg="#2C3E50", fg="white", padx=20)
        close_button.pack(pady=10)
        
        print("✅ GUI test window opened")
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🏛️ Law Office Management System - Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_python_version():
        return False
    
    if not check_tkinter():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test components
    if not test_arabic_support():
        print("⚠️  Warning: Arabic support may not work properly")
    
    if not test_database():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  python main.py")
    print("or")
    print("  Double-click run_law_office.bat (Windows)")
    print("\nDefault login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 50)
    
    # Show GUI test
    try:
        response = input("\nWould you like to run a GUI test? (y/n): ").lower()
        if response in ['y', 'yes']:
            show_gui_test()
    except KeyboardInterrupt:
        print("\nSetup completed.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)