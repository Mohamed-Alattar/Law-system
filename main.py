#!/usr/bin/env python3
"""
Law Office Management System
Main Entry Point

A comprehensive law office management system for Egyptian law firms.
Supports Arabic and English languages with RTL layout for Arabic.

Features:
- Case Management
- Client Management  
- Task and Appointment Management
- Document Archiving
- Billing and Accounting
- Reports and Statistics
- User Management with Role-based Access Control
- Backup and Restore
- Multi-language Support (Arabic/English)

Author: Assistant
Version: 1.0.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import sqlite3
    except ImportError:
        missing_deps.append("sqlite3")
    
    try:
        import bcrypt
    except ImportError:
        missing_deps.append("bcrypt")
    
    try:
        import arabic_reshaper
    except ImportError:
        missing_deps.append("arabic-reshaper")
    
    try:
        import bidi
    except ImportError:
        missing_deps.append("python-bidi")
    
    if missing_deps:
        error_msg = f"Missing required dependencies: {', '.join(missing_deps)}\n"
        error_msg += "Please install them using: pip install " + " ".join(missing_deps)
        
        # Show error in GUI if possible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", error_msg)
            root.destroy()
        except:
            print(error_msg)
        
        return False
    
    return True

def main():
    """Main application entry point"""
    try:
        # Check dependencies first
        if not check_dependencies():
            sys.exit(1)
        
        # Import and initialize the application
        from login_window import LoginWindow
        
        # Start the application
        app = LoginWindow()
        app.run()
        
    except ImportError as e:
        error_msg = f"Import error: {str(e)}\nPlease ensure all required files are present."
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Import Error", error_msg)
            root.destroy()
        except:
            print(error_msg)
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Application error: {str(e)}"
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
            root.destroy()
        except:
            print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()