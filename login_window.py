"""
Login Window for Law Office Management System
"""
import tkinter as tk
from tkinter import ttk
from gui_components import *
from auth import auth
from i18n import i18n
from config import *

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Setup the login window"""
        self.root.title(RTLWidget.format_text(i18n.get('app_title')))
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Set background color
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def create_widgets(self):
        """Create login form widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Logo/Title frame
        title_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        title_frame.pack(pady=(0, 30))
        
        # App title
        StyledLabel(
            title_frame, 
            text=i18n.get('app_title'),
            style="title"
        ).pack()
        
        # Subtitle
        StyledLabel(
            title_frame,
            text=i18n.get('login'),
            style="header"
        ).pack(pady=(10, 0))
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        form_frame.pack(fill="x", pady=20)
        
        # Username field
        username_frame = tk.Frame(form_frame, bg=BACKGROUND_COLOR)
        username_frame.pack(fill="x", pady=(0, 15))
        
        StyledLabel(username_frame, text=i18n.get('username')).pack(
            anchor="e" if i18n.is_rtl() else "w"
        )
        
        self.username_var = tk.StringVar()
        self.username_entry = StyledEntry(
            username_frame, 
            textvariable=self.username_var,
            font=RTLWidget.get_font(14)
        )
        self.username_entry.pack(fill="x", pady=(5, 0), ipady=8)
        
        # Password field
        password_frame = tk.Frame(form_frame, bg=BACKGROUND_COLOR)
        password_frame.pack(fill="x", pady=(0, 20))
        
        StyledLabel(password_frame, text=i18n.get('password')).pack(
            anchor="e" if i18n.is_rtl() else "w"
        )
        
        self.password_var = tk.StringVar()
        self.password_entry = StyledEntry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            font=RTLWidget.get_font(14)
        )
        self.password_entry.pack(fill="x", pady=(5, 0), ipady=8)
        
        # Language selection
        lang_frame = tk.Frame(form_frame, bg=BACKGROUND_COLOR)
        lang_frame.pack(fill="x", pady=(0, 20))
        
        StyledLabel(lang_frame, text=i18n.get('language')).pack(
            anchor="e" if i18n.is_rtl() else "w"
        )
        
        self.language_var = tk.StringVar(value=i18n.current_language)
        language_combo = StyledCombobox(
            lang_frame,
            textvariable=self.language_var,
            values=['ar', 'en'],
            state="readonly"
        )
        language_combo.pack(fill="x", pady=(5, 0))
        language_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg=BACKGROUND_COLOR)
        buttons_frame.pack(fill="x")
        
        # Login button
        self.login_button = StyledButton(
            buttons_frame,
            text=i18n.get('login_button'),
            command=self.login,
            style="primary"
        )
        self.login_button.pack(fill="x", ipady=10)
        
        # Error message label
        self.error_label = StyledLabel(
            main_frame,
            text="",
            fg=DANGER_COLOR
        )
        self.error_label.pack(pady=(10, 0))
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
        
        # Default credentials info
        info_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        info_frame.pack(side="bottom", pady=(20, 0))
        
        StyledLabel(
            info_frame,
            text="Default: admin / admin123",
            fg="#7F8C8D",
            font=RTLWidget.get_font(10)
        ).pack()
    
    def change_language(self, event=None):
        """Change application language"""
        new_lang = self.language_var.get()
        i18n.set_language(new_lang)
        
        # Recreate the window with new language
        self.root.destroy()
        self.__init__()
    
    def login(self):
        """Handle login attempt"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        # Clear previous error
        self.error_label.config(text="")
        
        # Validate input
        if not username or not password:
            self.show_error(i18n.get('invalid_input'))
            return
        
        # Disable login button during authentication
        self.login_button.config(state="disabled")
        self.root.update()
        
        try:
            # Attempt authentication
            if auth.authenticate(username, password):
                self.root.destroy()
                # Import and start main application
                from main_window import MainWindow
                MainWindow()
            else:
                self.show_error(i18n.get('invalid_credentials'))
        except Exception as e:
            self.show_error(f"{i18n.get('login_failed')}: {str(e)}")
        finally:
            self.login_button.config(state="normal")
    
    def show_error(self, message):
        """Show error message"""
        self.error_label.config(text=RTLWidget.format_text(message))
    
    def run(self):
        """Start the login window"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.run()