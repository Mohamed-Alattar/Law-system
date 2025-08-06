"""
GUI Components and Widgets with Arabic/RTL support
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkFont
from datetime import datetime, date
import arabic_reshaper
from bidi.algorithm import get_display
from config import *
from i18n import i18n

class RTLWidget:
    """Base class for RTL (Right-to-Left) widget support"""
    
    @staticmethod
    def format_text(text):
        """Format Arabic text for proper display"""
        if not text:
            return ""
        
        if i18n.is_rtl():
            try:
                # Reshape Arabic text and apply BiDi algorithm
                reshaped_text = arabic_reshaper.reshape(str(text))
                bidi_text = get_display(reshaped_text)
                return bidi_text
            except:
                return str(text)
        return str(text)
    
    @staticmethod
    def get_font(size=FONT_SIZE_NORMAL, weight="normal"):
        """Get appropriate font based on current language"""
        if i18n.is_rtl():
            family = FONT_FAMILY_AR
        else:
            family = FONT_FAMILY_EN
        
        return (family, size, weight)

class StyledButton(tk.Button):
    """Styled button with RTL support"""
    
    def __init__(self, parent, text="", command=None, style="primary", **kwargs):
        # Set default styling
        if style == "primary":
            bg = PRIMARY_COLOR
            fg = "white"
            active_bg = SECONDARY_COLOR
        elif style == "secondary":
            bg = SECONDARY_COLOR
            fg = "white"
            active_bg = PRIMARY_COLOR
        elif style == "success":
            bg = SUCCESS_COLOR
            fg = "white"
            active_bg = "#229954"
        elif style == "danger":
            bg = DANGER_COLOR
            fg = "white"
            active_bg = "#CB4335"
        else:
            bg = BACKGROUND_COLOR
            fg = TEXT_COLOR
            active_bg = "#D5DBDB"
        
        # Format text for RTL
        formatted_text = RTLWidget.format_text(text)
        font = RTLWidget.get_font()
        
        # Create button with styling
        super().__init__(
            parent,
            text=formatted_text,
            command=command,
            font=font,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            **kwargs
        )

class StyledLabel(tk.Label):
    """Styled label with RTL support"""
    
    def __init__(self, parent, text="", style="normal", **kwargs):
        # Set font size based on style
        if style == "title":
            font = RTLWidget.get_font(FONT_SIZE_TITLE, "bold")
        elif style == "header":
            font = RTLWidget.get_font(FONT_SIZE_HEADER, "bold")
        else:
            font = RTLWidget.get_font()
        
        # Format text for RTL
        formatted_text = RTLWidget.format_text(text)
        
        # Set text anchor based on language direction
        anchor = "e" if i18n.is_rtl() else "w"
        
        super().__init__(
            parent,
            text=formatted_text,
            font=font,
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            anchor=anchor,
            **kwargs
        )

class StyledEntry(tk.Entry):
    """Styled entry with RTL support"""
    
    def __init__(self, parent, **kwargs):
        font = RTLWidget.get_font()
        
        # Set text alignment based on language direction
        justify = "right" if i18n.is_rtl() else "left"
        
        super().__init__(
            parent,
            font=font,
            justify=justify,
            relief="solid",
            borderwidth=1,
            **kwargs
        )

class StyledText(tk.Text):
    """Styled text widget with RTL support"""
    
    def __init__(self, parent, **kwargs):
        font = RTLWidget.get_font()
        
        super().__init__(
            parent,
            font=font,
            wrap=tk.WORD,
            relief="solid",
            borderwidth=1,
            **kwargs
        )
        
        # Configure tags for RTL text
        if i18n.is_rtl():
            self.tag_configure("rtl", justify="right")
            self.tag_add("rtl", "1.0", "end")

class StyledCombobox(ttk.Combobox):
    """Styled combobox with RTL support"""
    
    def __init__(self, parent, values=None, **kwargs):
        if values:
            # Format values for RTL
            formatted_values = [RTLWidget.format_text(str(val)) for val in values]
            kwargs['values'] = formatted_values
        
        super().__init__(parent, **kwargs)
        
        # Set font
        font = RTLWidget.get_font()
        self.configure(font=font)

class DataTreeview(ttk.Treeview):
    """Enhanced Treeview with RTL support and additional features"""
    
    def __init__(self, parent, columns=None, **kwargs):
        super().__init__(parent, columns=columns, **kwargs)
        
        # Configure font
        font = RTLWidget.get_font()
        self.configure(font=font)
        
        # Configure headings with RTL support
        if columns:
            for col in columns:
                self.heading(col, text=RTLWidget.format_text(col))
                # Set anchor based on language direction
                anchor = "e" if i18n.is_rtl() else "w"
                self.column(col, anchor=anchor)
    
    def insert_data(self, data_list, format_rtl=True):
        """Insert data with RTL formatting"""
        for item in data_list:
            if format_rtl:
                formatted_item = [RTLWidget.format_text(str(val)) if val else "" for val in item]
            else:
                formatted_item = [str(val) if val else "" for val in item]
            
            self.insert("", "end", values=formatted_item)

class DatePicker(tk.Frame):
    """Date picker widget with RTL support"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.date_var = tk.StringVar()
        
        # Create date entry
        self.date_entry = StyledEntry(self, textvariable=self.date_var, width=12)
        self.date_entry.pack(side="right" if i18n.is_rtl() else "left", fill="x", expand=True)
        
        # Calendar button
        self.cal_button = StyledButton(
            self, 
            text="📅", 
            command=self.open_calendar,
            style="secondary"
        )
        self.cal_button.pack(side="left" if i18n.is_rtl() else "right", padx=(5, 0))
        
        # Set current date
        self.set_date(date.today())
    
    def open_calendar(self):
        """Open calendar popup"""
        try:
            from tkcalendar import DateEntry
            
            # Create popup window
            popup = tk.Toplevel(self)
            popup.title(i18n.get('select_date', 'Select Date'))
            popup.geometry("250x200")
            popup.transient(self)
            popup.grab_set()
            
            # Create calendar
            cal = DateEntry(
                popup,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='dd/mm/yyyy'
            )
            cal.pack(padx=10, pady=10)
            
            def select_date():
                self.set_date(cal.get_date())
                popup.destroy()
            
            # Buttons
            btn_frame = tk.Frame(popup)
            btn_frame.pack(pady=10)
            
            StyledButton(btn_frame, text=i18n.get('ok'), command=select_date).pack(side="left", padx=5)
            StyledButton(btn_frame, text=i18n.get('cancel'), command=popup.destroy).pack(side="left", padx=5)
            
        except ImportError:
            # Fallback to simple date input
            date_str = self.date_var.get()
            new_date = tk.simpledialog.askstring(
                i18n.get('select_date', 'Select Date'),
                i18n.get('enter_date', 'Enter date (DD/MM/YYYY):'),
                initialvalue=date_str
            )
            if new_date:
                try:
                    parsed_date = datetime.strptime(new_date, "%d/%m/%Y").date()
                    self.set_date(parsed_date)
                except ValueError:
                    messagebox.showerror(i18n.get('error'), i18n.get('invalid_date_format'))
    
    def set_date(self, date_obj):
        """Set date value"""
        if isinstance(date_obj, str):
            self.date_var.set(date_obj)
        else:
            self.date_var.set(date_obj.strftime("%d/%m/%Y"))
    
    def get_date(self):
        """Get date value as date object"""
        try:
            date_str = self.date_var.get()
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            return None
    
    def get_date_string(self):
        """Get date value as string"""
        return self.date_var.get()

class SearchFrame(tk.Frame):
    """Search frame with RTL support"""
    
    def __init__(self, parent, search_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.search_callback = search_callback
        
        # Search label
        StyledLabel(self, text=i18n.get('search')).pack(
            side="right" if i18n.is_rtl() else "left", 
            padx=(0, 5)
        )
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = StyledEntry(self, textvariable=self.search_var, width=30)
        self.search_entry.pack(
            side="right" if i18n.is_rtl() else "left", 
            fill="x", 
            expand=True, 
            padx=(0, 5)
        )
        
        # Search button
        StyledButton(
            self, 
            text=i18n.get('search'), 
            command=self.perform_search,
            style="secondary"
        ).pack(side="right" if i18n.is_rtl() else "left")
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
    
    def perform_search(self):
        """Perform search"""
        if self.search_callback:
            self.search_callback(self.search_var.get())
    
    def get_search_text(self):
        """Get search text"""
        return self.search_var.get()
    
    def clear_search(self):
        """Clear search text"""
        self.search_var.set("")

class StatusBar(tk.Frame):
    """Status bar widget"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, relief="sunken", bd=1, **kwargs)
        
        self.status_var = tk.StringVar()
        self.status_var.set(i18n.get('ready', 'Ready'))
        
        self.label = StyledLabel(self, textvariable=self.status_var)
        self.label.pack(side="left", padx=5)
    
    def set_status(self, message):
        """Set status message"""
        self.status_var.set(RTLWidget.format_text(message))
    
    def clear_status(self):
        """Clear status message"""
        self.status_var.set(i18n.get('ready', 'Ready'))

def show_message(title, message, msg_type="info"):
    """Show message dialog with RTL support"""
    formatted_title = RTLWidget.format_text(title)
    formatted_message = RTLWidget.format_text(message)
    
    if msg_type == "error":
        messagebox.showerror(formatted_title, formatted_message)
    elif msg_type == "warning":
        messagebox.showwarning(formatted_title, formatted_message)
    elif msg_type == "question":
        return messagebox.askyesno(formatted_title, formatted_message)
    else:
        messagebox.showinfo(formatted_title, formatted_message)

def show_error(message):
    """Show error message"""
    show_message(i18n.get('error'), message, "error")

def show_success(message):
    """Show success message"""
    show_message(i18n.get('success'), message, "info")

def show_warning(message):
    """Show warning message"""
    show_message(i18n.get('warning'), message, "warning")

def confirm_action(message):
    """Show confirmation dialog"""
    return show_message(i18n.get('confirm'), message, "question")