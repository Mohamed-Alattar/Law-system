#!/usr/bin/env python3
"""
Quick installation test for Law Office Management System
Run this script to verify all components are working properly
"""

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import tkinter
        print("✅ tkinter")
    except ImportError:
        print("❌ tkinter - Not available")
        return False
    
    try:
        import sqlite3
        print("✅ sqlite3")
    except ImportError:
        print("❌ sqlite3 - Not available")
        return False
    
    try:
        import bcrypt
        print("✅ bcrypt")
    except ImportError:
        print("❌ bcrypt - Run: pip install bcrypt")
        return False
    
    try:
        import arabic_reshaper
        print("✅ arabic_reshaper")
    except ImportError:
        print("❌ arabic_reshaper - Run: pip install arabic-reshaper")
        return False
    
    try:
        from bidi.algorithm import get_display
        print("✅ python-bidi")
    except ImportError:
        print("❌ python-bidi - Run: pip install python-bidi")
        return False
    
    return True

def test_arabic_rendering():
    """Test Arabic text rendering"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        test_text = "نظام إدارة مكتب المحاماة"
        reshaped = arabic_reshaper.reshape(test_text)
        bidi_text = get_display(reshaped)
        
        print("✅ Arabic text rendering works")
        print(f"   Original: {test_text}")
        print(f"   Rendered: {bidi_text}")
        return True
    except Exception as e:
        print(f"❌ Arabic rendering failed: {e}")
        return False

def test_gui():
    """Test basic GUI functionality"""
    try:
        import tkinter as tk
        
        # Create a simple test window
        root = tk.Tk()
        root.title("Test")
        root.geometry("300x100")
        
        # Test if we can create widgets
        label = tk.Label(root, text="GUI Test Successful!")
        label.pack(pady=20)
        
        # Close immediately
        root.after(100, root.destroy)
        root.mainloop()
        
        print("✅ GUI functionality works")
        return True
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Law Office Management System - Installation Test")
    print("=" * 60)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    print()
    
    # Test Arabic rendering
    if not test_arabic_rendering():
        success = False
    
    print()
    
    # Test GUI
    if not test_gui():
        success = False
    
    print()
    print("=" * 60)
    
    if success:
        print("🎉 All tests passed! The system should work properly.")
        print("You can now run: python main.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("Try running: python setup.py")
    
    print("=" * 60)

if __name__ == "__main__":
    main()