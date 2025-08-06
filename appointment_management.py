"""
Appointment Management Module for Law Office Management System
"""
import tkinter as tk
from gui_components import *
from i18n import i18n

class AppointmentManagement:
    def __init__(self, parent):
        self.parent = parent
        self.create_interface()
    
    def create_interface(self):
        """Create the appointment management interface"""
        # Main frame
        main_frame = tk.Frame(self.parent, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        StyledLabel(main_frame, text=i18n.get('appointment_management'), style="title").pack(
            anchor="e" if i18n.is_rtl() else "w", pady=(0, 20)
        )
        
        # Placeholder content
        placeholder_frame = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
        placeholder_frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        StyledLabel(
            placeholder_frame, 
            text=i18n.get('coming_soon', 'Appointment Management - Coming Soon'),
            style="header"
        ).pack(expand=True)
        
        StyledLabel(
            placeholder_frame,
            text=i18n.get('appointment_management_desc', 'This module will include calendar view, appointment scheduling, and reminders.')
        ).pack(expand=True, pady=10)