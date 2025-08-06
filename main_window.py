"""
Main Application Window for Law Office Management System
"""
import tkinter as tk
from tkinter import ttk
from gui_components import *
from auth import auth
from i18n import i18n
from config import *
import os

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.current_module = None
        self.setup_window()
        self.create_menu()
        self.create_main_interface()
        self.show_dashboard()
        self.root.mainloop()
    
    def setup_window(self):
        """Setup the main window"""
        self.root.title(RTLWidget.format_text(f"{i18n.get('app_title')} - {auth.get_current_user()['full_name']}"))
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=RTLWidget.format_text(i18n.get('file', 'File')), menu=file_menu)
        file_menu.add_command(label=RTLWidget.format_text(i18n.get('backup_database', 'Backup Database')), command=self.backup_database)
        file_menu.add_command(label=RTLWidget.format_text(i18n.get('restore_database', 'Restore Database')), command=self.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label=RTLWidget.format_text(i18n.get('logout')), command=self.logout)
        file_menu.add_command(label=RTLWidget.format_text(i18n.get('exit', 'Exit')), command=self.on_closing)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=RTLWidget.format_text(i18n.get('settings')), menu=settings_menu)
        settings_menu.add_command(label=RTLWidget.format_text(i18n.get('change_language', 'Change Language')), command=self.change_language)
        if auth.can_manage_users():
            settings_menu.add_command(label=RTLWidget.format_text(i18n.get('user_management')), command=self.show_user_management)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=RTLWidget.format_text(i18n.get('help', 'Help')), menu=help_menu)
        help_menu.add_command(label=RTLWidget.format_text(i18n.get('about', 'About')), command=self.show_about)
    
    def create_main_interface(self):
        """Create the main interface layout"""
        # Create main container
        main_container = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create sidebar for navigation
        self.sidebar = tk.Frame(main_container, bg=PRIMARY_COLOR, width=250)
        self.sidebar.pack(side="right" if i18n.is_rtl() else "left", fill="y", padx=(0, 10) if not i18n.is_rtl() else (10, 0))
        self.sidebar.pack_propagate(False)
        
        # Create content area
        self.content_frame = tk.Frame(main_container, bg="white", relief="solid", bd=1)
        self.content_frame.pack(side="left" if i18n.is_rtl() else "right", fill="both", expand=True)
        
        # Create sidebar content
        self.create_sidebar()
        
        # Create status bar
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side="bottom", fill="x")
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        # Header
        header_frame = tk.Frame(self.sidebar, bg=PRIMARY_COLOR)
        header_frame.pack(fill="x", pady=(20, 30))
        
        # User info
        user = auth.get_current_user()
        StyledLabel(
            header_frame,
            text=user['full_name'],
            fg="white",
            bg=PRIMARY_COLOR,
            style="header"
        ).pack()
        
        StyledLabel(
            header_frame,
            text=i18n.get(user['role']),
            fg="#BDC3C7",
            bg=PRIMARY_COLOR
        ).pack()
        
        # Navigation buttons
        nav_frame = tk.Frame(self.sidebar, bg=PRIMARY_COLOR)
        nav_frame.pack(fill="both", expand=True, padx=10)
        
        # Dashboard
        self.create_nav_button(nav_frame, i18n.get('dashboard'), self.show_dashboard, "📊")
        
        # Cases
        if auth.can_manage_cases():
            self.create_nav_button(nav_frame, i18n.get('cases'), self.show_cases, "⚖️")
        
        # Clients
        self.create_nav_button(nav_frame, i18n.get('clients'), self.show_clients, "👥")
        
        # Tasks
        self.create_nav_button(nav_frame, i18n.get('tasks'), self.show_tasks, "📝")
        
        # Appointments
        self.create_nav_button(nav_frame, i18n.get('appointments'), self.show_appointments, "📅")
        
        # Documents
        self.create_nav_button(nav_frame, i18n.get('documents'), self.show_documents, "📄")
        
        # Billing
        if auth.can_view_financial_reports():
            self.create_nav_button(nav_frame, i18n.get('billing'), self.show_billing, "💰")
        
        # Reports
        if auth.can_view_financial_reports():
            self.create_nav_button(nav_frame, i18n.get('reports'), self.show_reports, "📈")
    
    def create_nav_button(self, parent, text, command, icon=""):
        """Create a navigation button"""
        btn_frame = tk.Frame(parent, bg=PRIMARY_COLOR)
        btn_frame.pack(fill="x", pady=2)
        
        btn_text = f"{icon} {text}" if icon else text
        
        btn = tk.Button(
            btn_frame,
            text=RTLWidget.format_text(btn_text),
            command=command,
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=SECONDARY_COLOR,
            activeforeground="white",
            relief="flat",
            font=RTLWidget.get_font(12),
            anchor="e" if i18n.is_rtl() else "w",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn.pack(fill="x")
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=SECONDARY_COLOR)
        
        def on_leave(e):
            btn.config(bg=PRIMARY_COLOR)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard"""
        self.clear_content()
        self.current_module = "dashboard"
        self.status_bar.set_status(i18n.get('dashboard'))
        
        # Create dashboard
        dashboard = tk.Frame(self.content_frame, bg="white")
        dashboard.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        StyledLabel(dashboard, text=i18n.get('dashboard'), style="title").pack(anchor="e" if i18n.is_rtl() else "w", pady=(0, 20))
        
        # Statistics cards
        stats_frame = tk.Frame(dashboard, bg="white")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        self.create_stats_cards(stats_frame)
        
        # Recent activities
        recent_frame = tk.Frame(dashboard, bg="white")
        recent_frame.pack(fill="both", expand=True)
        
        StyledLabel(recent_frame, text=i18n.get('recent_activities', 'Recent Activities'), style="header").pack(anchor="e" if i18n.is_rtl() else "w", pady=(0, 10))
        
        # Activities list
        activities_list = DataTreeview(
            recent_frame,
            columns=('type', 'description', 'date'),
            show='headings'
        )
        
        activities_list.heading('type', text=RTLWidget.format_text(i18n.get('type', 'Type')))
        activities_list.heading('description', text=RTLWidget.format_text(i18n.get('description')))
        activities_list.heading('date', text=RTLWidget.format_text(i18n.get('date', 'Date')))
        
        activities_list.pack(fill="both", expand=True)
        
        # Load recent activities
        self.load_recent_activities(activities_list)
    
    def create_stats_cards(self, parent):
        """Create statistics cards"""
        from database import db
        
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get statistics
                cursor.execute("SELECT COUNT(*) FROM cases WHERE status = 'open'")
                open_cases = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM clients")
                total_clients = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
                pending_tasks = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date >= datetime('now') AND status = 'scheduled'")
                upcoming_appointments = cursor.fetchone()[0]
                
                # Create cards
                cards_data = [
                    (i18n.get('open_cases', 'Open Cases'), open_cases, SUCCESS_COLOR, "⚖️"),
                    (i18n.get('total_clients', 'Total Clients'), total_clients, SECONDARY_COLOR, "👥"),
                    (i18n.get('pending_tasks', 'Pending Tasks'), pending_tasks, WARNING_COLOR, "📝"),
                    (i18n.get('upcoming_appointments', 'Upcoming Appointments'), upcoming_appointments, PRIMARY_COLOR, "📅")
                ]
                
                for i, (title, value, color, icon) in enumerate(cards_data):
                    card = self.create_stat_card(parent, title, value, color, icon)
                    card.grid(row=0, column=i, padx=10, sticky="ew")
                
                # Configure grid weights
                for i in range(len(cards_data)):
                    parent.grid_columnconfigure(i, weight=1)
                    
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def create_stat_card(self, parent, title, value, color, icon):
        """Create a single statistics card"""
        card = tk.Frame(parent, bg=color, relief="solid", bd=1)
        
        # Icon and value
        top_frame = tk.Frame(card, bg=color)
        top_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        tk.Label(
            top_frame,
            text=icon,
            bg=color,
            fg="white",
            font=RTLWidget.get_font(24)
        ).pack(side="right" if i18n.is_rtl() else "left")
        
        tk.Label(
            top_frame,
            text=str(value),
            bg=color,
            fg="white",
            font=RTLWidget.get_font(28, "bold")
        ).pack(side="left" if i18n.is_rtl() else "right")
        
        # Title
        tk.Label(
            card,
            text=RTLWidget.format_text(title),
            bg=color,
            fg="white",
            font=RTLWidget.get_font(12),
            anchor="e" if i18n.is_rtl() else "w"
        ).pack(fill="x", padx=15, pady=(0, 15))
        
        return card
    
    def load_recent_activities(self, tree):
        """Load recent activities into the tree"""
        # Mock data for now - in real implementation, this would load from database
        activities = [
            ('Case', 'New case added: Commercial Dispute', '2024-01-20'),
            ('Client', 'New client registered: Ahmed Hassan', '2024-01-19'),
            ('Task', 'Task completed: Document review', '2024-01-18'),
            ('Appointment', 'Appointment scheduled with client', '2024-01-17'),
        ]
        
        for activity in activities:
            tree.insert("", "end", values=[RTLWidget.format_text(str(val)) for val in activity])
    
    def show_cases(self):
        """Show cases management"""
        self.clear_content()
        self.current_module = "cases"
        self.status_bar.set_status(i18n.get('case_management'))
        
        from case_management import CaseManagement
        CaseManagement(self.content_frame)
    
    def show_clients(self):
        """Show clients management"""
        self.clear_content()
        self.current_module = "clients"
        self.status_bar.set_status(i18n.get('client_management'))
        
        from client_management import ClientManagement
        ClientManagement(self.content_frame)
    
    def show_tasks(self):
        """Show tasks management"""
        self.clear_content()
        self.current_module = "tasks"
        self.status_bar.set_status(i18n.get('task_management'))
        
        from task_management import TaskManagement
        TaskManagement(self.content_frame)
    
    def show_appointments(self):
        """Show appointments management"""
        self.clear_content()
        self.current_module = "appointments"
        self.status_bar.set_status(i18n.get('appointment_management'))
        
        from appointment_management import AppointmentManagement
        AppointmentManagement(self.content_frame)
    
    def show_documents(self):
        """Show documents management"""
        self.clear_content()
        self.current_module = "documents"
        self.status_bar.set_status(i18n.get('document_management'))
        
        from document_management import DocumentManagement
        DocumentManagement(self.content_frame)
    
    def show_billing(self):
        """Show billing management"""
        self.clear_content()
        self.current_module = "billing"
        self.status_bar.set_status(i18n.get('billing_management'))
        
        from billing_management import BillingManagement
        BillingManagement(self.content_frame)
    
    def show_reports(self):
        """Show reports"""
        self.clear_content()
        self.current_module = "reports"
        self.status_bar.set_status(i18n.get('reports_statistics'))
        
        from reports import ReportsModule
        ReportsModule(self.content_frame)
    
    def show_user_management(self):
        """Show user management"""
        self.clear_content()
        self.current_module = "users"
        self.status_bar.set_status(i18n.get('user_management'))
        
        from user_management_ui import UserManagementUI
        UserManagementUI(self.content_frame)
    
    def backup_database(self):
        """Create database backup"""
        try:
            from database import db
            backup_path = db.backup_database()
            if backup_path:
                show_success(f"{i18n.get('backup_created')}\n{backup_path}")
            else:
                show_error(i18n.get('backup_failed', 'Backup failed'))
        except Exception as e:
            show_error(f"{i18n.get('backup_failed', 'Backup failed')}: {str(e)}")
    
    def restore_database(self):
        """Restore database from backup"""
        try:
            filename = filedialog.askopenfilename(
                title=RTLWidget.format_text(i18n.get('select_backup_file', 'Select Backup File')),
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if filename:
                if confirm_action(i18n.get('confirm_restore', 'This will replace current data. Continue?')):
                    from database import db
                    if db.restore_database(filename):
                        show_success(i18n.get('backup_restored'))
                        # Restart application
                        self.root.destroy()
                        from login_window import LoginWindow
                        LoginWindow()
                    else:
                        show_error(i18n.get('restore_failed', 'Restore failed'))
        except Exception as e:
            show_error(f"{i18n.get('restore_failed', 'Restore failed')}: {str(e)}")
    
    def change_language(self):
        """Change application language"""
        # Create language selection dialog
        lang_window = tk.Toplevel(self.root)
        lang_window.title(RTLWidget.format_text(i18n.get('change_language')))
        lang_window.geometry("300x150")
        lang_window.transient(self.root)
        lang_window.grab_set()
        
        # Center the window
        lang_window.update_idletasks()
        x = (lang_window.winfo_screenwidth() // 2) - (150)
        y = (lang_window.winfo_screenheight() // 2) - (75)
        lang_window.geometry(f"300x150+{x}+{y}")
        
        frame = tk.Frame(lang_window, bg=BACKGROUND_COLOR)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        StyledLabel(frame, text=i18n.get('select_language', 'Select Language')).pack()
        
        lang_var = tk.StringVar(value=i18n.current_language)
        lang_combo = StyledCombobox(frame, textvariable=lang_var, values=['ar', 'en'], state="readonly")
        lang_combo.pack(fill="x", pady=10)
        
        def apply_language():
            i18n.set_language(lang_var.get())
            lang_window.destroy()
            # Restart application
            self.root.destroy()
            from login_window import LoginWindow
            LoginWindow()
        
        StyledButton(frame, text=i18n.get('apply', 'Apply'), command=apply_language).pack(pady=10)
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""{i18n.get('app_title')}
{i18n.get('version', 'Version')}: {APP_VERSION}

{i18n.get('description', 'A comprehensive law office management system for Egyptian law firms.')}
        """
        show_message(i18n.get('about'), about_text)
    
    def logout(self):
        """Logout and return to login screen"""
        if confirm_action(i18n.get('confirm_logout', 'Are you sure you want to logout?')):
            auth.logout()
            self.root.destroy()
            from login_window import LoginWindow
            LoginWindow()
    
    def on_closing(self):
        """Handle window close event"""
        if confirm_action(i18n.get('confirm_exit', 'Are you sure you want to exit?')):
            self.root.quit()

if __name__ == "__main__":
    # This should not be called directly - use login_window.py
    pass