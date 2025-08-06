"""
Case Management Module for Law Office Management System
"""
import tkinter as tk
from tkinter import ttk
from gui_components import *
from database import db
from auth import auth
from i18n import i18n
from datetime import datetime, date

class CaseManagement:
    def __init__(self, parent):
        self.parent = parent
        self.current_case = None
        self.create_interface()
        self.load_cases()
    
    def create_interface(self):
        """Create the case management interface"""
        # Main frame
        main_frame = tk.Frame(self.parent, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 20))
        
        StyledLabel(header_frame, text=i18n.get('case_management'), style="title").pack(
            side="right" if i18n.is_rtl() else "left"
        )
        
        # Buttons frame
        buttons_frame = tk.Frame(header_frame, bg="white")
        buttons_frame.pack(side="left" if i18n.is_rtl() else "right")
        
        StyledButton(
            buttons_frame,
            text=i18n.get('add_case'),
            command=self.add_case,
            style="success"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('edit'),
            command=self.edit_case,
            style="primary"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('delete'),
            command=self.delete_case,
            style="danger"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('refresh'),
            command=self.load_cases,
            style="secondary"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        # Search frame
        search_frame = SearchFrame(main_frame, self.search_cases)
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Cases list
        list_frame = tk.Frame(main_frame, bg="white")
        list_frame.pack(fill="both", expand=True)
        
        # Create treeview for cases
        columns = (
            i18n.get('case_number'),
            i18n.get('case_title'),
            i18n.get('client_name'),
            i18n.get('court_name'),
            i18n.get('case_type'),
            i18n.get('case_status'),
            i18n.get('assigned_lawyer'),
            i18n.get('start_date')
        )
        
        self.cases_tree = DataTreeview(list_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.cases_tree.heading(col, text=RTLWidget.format_text(col))
            self.cases_tree.column(col, width=120, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.cases_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.cases_tree.xview)
        
        self.cases_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.cases_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click to edit
        self.cases_tree.bind('<Double-1>', lambda e: self.edit_case())
        
        # Bind selection
        self.cases_tree.bind('<<TreeviewSelect>>', self.on_case_select)
    
    def load_cases(self):
        """Load cases from database"""
        try:
            # Clear existing items
            for item in self.cases_tree.get_children():
                self.cases_tree.delete(item)
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Join with clients and users tables to get names
                query = '''
                    SELECT 
                        c.id,
                        c.case_number,
                        c.title,
                        cl.name as client_name,
                        c.court_name,
                        c.case_type,
                        c.status,
                        u.full_name as lawyer_name,
                        c.start_date
                    FROM cases c
                    LEFT JOIN clients cl ON c.client_id = cl.id
                    LEFT JOIN users u ON c.assigned_lawyer_id = u.id
                    ORDER BY c.created_at DESC
                '''
                
                cursor.execute(query)
                cases = cursor.fetchall()
                
                for case in cases:
                    # Format data for display
                    case_data = [
                        case['case_number'] or '',
                        case['title'] or '',
                        case['client_name'] or '',
                        case['court_name'] or '',
                        case['case_type'] or '',
                        i18n.get(case['status'], case['status']) if case['status'] else '',
                        case['lawyer_name'] or '',
                        self.format_date(case['start_date']) if case['start_date'] else ''
                    ]
                    
                    # Insert with RTL formatting
                    formatted_data = [RTLWidget.format_text(str(val)) for val in case_data]
                    item = self.cases_tree.insert("", "end", values=formatted_data)
                    
                    # Store case ID in item
                    self.cases_tree.set(item, '#1', case['id'])
                    
        except Exception as e:
            show_error(f"Error loading cases: {str(e)}")
    
    def search_cases(self, search_term):
        """Search cases"""
        if not search_term.strip():
            self.load_cases()
            return
        
        try:
            # Clear existing items
            for item in self.cases_tree.get_children():
                self.cases_tree.delete(item)
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                search_pattern = f"%{search_term}%"
                query = '''
                    SELECT 
                        c.id,
                        c.case_number,
                        c.title,
                        cl.name as client_name,
                        c.court_name,
                        c.case_type,
                        c.status,
                        u.full_name as lawyer_name,
                        c.start_date
                    FROM cases c
                    LEFT JOIN clients cl ON c.client_id = cl.id
                    LEFT JOIN users u ON c.assigned_lawyer_id = u.id
                    WHERE c.case_number LIKE ? OR c.title LIKE ? OR cl.name LIKE ?
                    ORDER BY c.created_at DESC
                '''
                
                cursor.execute(query, (search_pattern, search_pattern, search_pattern))
                cases = cursor.fetchall()
                
                for case in cases:
                    case_data = [
                        case['case_number'] or '',
                        case['title'] or '',
                        case['client_name'] or '',
                        case['court_name'] or '',
                        case['case_type'] or '',
                        i18n.get(case['status'], case['status']) if case['status'] else '',
                        case['lawyer_name'] or '',
                        self.format_date(case['start_date']) if case['start_date'] else ''
                    ]
                    
                    formatted_data = [RTLWidget.format_text(str(val)) for val in case_data]
                    item = self.cases_tree.insert("", "end", values=formatted_data)
                    self.cases_tree.set(item, '#1', case['id'])
                    
        except Exception as e:
            show_error(f"Error searching cases: {str(e)}")
    
    def on_case_select(self, event):
        """Handle case selection"""
        selection = self.cases_tree.selection()
        if selection:
            item = selection[0]
            # The case ID is stored in the first column (hidden)
            self.current_case = self.cases_tree.item(item)['values'][0] if self.cases_tree.item(item)['values'] else None
    
    def add_case(self):
        """Add new case"""
        CaseDialog(self.parent, callback=self.load_cases)
    
    def edit_case(self):
        """Edit selected case"""
        if not self.current_case:
            show_warning(i18n.get('select_case_first', 'Please select a case first'))
            return
        
        try:
            # Get case ID from hidden column
            selection = self.cases_tree.selection()
            if not selection:
                show_warning(i18n.get('select_case_first', 'Please select a case first'))
                return
            
            # Get case ID from the tree item
            case_id = None
            for item in self.cases_tree.get_children():
                if item in selection:
                    # Try to get the case ID from the database based on case number
                    values = self.cases_tree.item(item)['values']
                    case_number = values[0] if values else None
                    
                    if case_number:
                        with db.get_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT id FROM cases WHERE case_number = ?", (case_number,))
                            result = cursor.fetchone()
                            if result:
                                case_id = result['id']
                    break
            
            if case_id:
                CaseDialog(self.parent, case_id=case_id, callback=self.load_cases)
            else:
                show_warning(i18n.get('case_not_found', 'Case not found'))
                
        except Exception as e:
            show_error(f"Error editing case: {str(e)}")
    
    def delete_case(self):
        """Delete selected case"""
        if not self.current_case:
            show_warning(i18n.get('select_case_first', 'Please select a case first'))
            return
        
        if not confirm_action(i18n.get('confirm_delete_case', 'Are you sure you want to delete this case?')):
            return
        
        try:
            # Get case ID similar to edit_case
            selection = self.cases_tree.selection()
            if not selection:
                return
            
            case_id = None
            for item in self.cases_tree.get_children():
                if item in selection:
                    values = self.cases_tree.item(item)['values']
                    case_number = values[0] if values else None
                    
                    if case_number:
                        with db.get_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT id FROM cases WHERE case_number = ?", (case_number,))
                            result = cursor.fetchone()
                            if result:
                                case_id = result['id']
                    break
            
            if case_id:
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
                    conn.commit()
                
                show_success(i18n.get('case_deleted', 'Case deleted successfully'))
                self.load_cases()
            else:
                show_warning(i18n.get('case_not_found', 'Case not found'))
                
        except Exception as e:
            show_error(f"Error deleting case: {str(e)}")
    
    def format_date(self, date_str):
        """Format date for display"""
        if not date_str:
            return ""
        
        try:
            # Parse date and format for display
            if isinstance(date_str, str):
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                parsed_date = date_str
            
            return parsed_date.strftime("%d/%m/%Y")
        except:
            return str(date_str)

class CaseDialog:
    def __init__(self, parent, case_id=None, callback=None):
        self.parent = parent
        self.case_id = case_id
        self.callback = callback
        self.clients = []
        self.lawyers = []
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(RTLWidget.format_text(i18n.get('edit_case') if case_id else i18n.get('add_case')))
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (300)
        y = (self.dialog.winfo_screenheight() // 2) - (350)
        self.dialog.geometry(f"600x700+{x}+{y}")
        
        self.create_form()
        self.load_data()
        
        if case_id:
            self.load_case_data()
    
    def create_form(self):
        """Create case form"""
        # Main frame with scrollbar
        canvas = tk.Canvas(self.dialog, bg="white")
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form content
        form_frame = tk.Frame(scrollable_frame, bg="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Case Number
        StyledLabel(form_frame, text=i18n.get('case_number')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.case_number_var = tk.StringVar()
        StyledEntry(form_frame, textvariable=self.case_number_var).pack(fill="x", pady=(5, 15))
        
        # Case Title
        StyledLabel(form_frame, text=i18n.get('case_title')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.title_var = tk.StringVar()
        StyledEntry(form_frame, textvariable=self.title_var).pack(fill="x", pady=(5, 15))
        
        # Client
        StyledLabel(form_frame, text=i18n.get('client_name')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.client_var = tk.StringVar()
        self.client_combo = StyledCombobox(form_frame, textvariable=self.client_var, state="readonly")
        self.client_combo.pack(fill="x", pady=(5, 15))
        
        # Court Name
        StyledLabel(form_frame, text=i18n.get('court_name')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.court_var = tk.StringVar()
        StyledEntry(form_frame, textvariable=self.court_var).pack(fill="x", pady=(5, 15))
        
        # Case Type
        StyledLabel(form_frame, text=i18n.get('case_type')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.case_type_var = tk.StringVar()
        case_types = ['Civil', 'Criminal', 'Commercial', 'Administrative', 'Family', 'Labor']
        self.case_type_combo = StyledCombobox(form_frame, textvariable=self.case_type_var, values=case_types)
        self.case_type_combo.pack(fill="x", pady=(5, 15))
        
        # Opponent Name
        StyledLabel(form_frame, text=i18n.get('opponent_name')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.opponent_var = tk.StringVar()
        StyledEntry(form_frame, textvariable=self.opponent_var).pack(fill="x", pady=(5, 15))
        
        # Status
        StyledLabel(form_frame, text=i18n.get('case_status')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.status_var = tk.StringVar(value="open")
        status_values = [('open', i18n.get('open')), ('closed', i18n.get('closed')), 
                        ('pending', i18n.get('pending')), ('postponed', i18n.get('postponed'))]
        status_display = [val[1] for val in status_values]
        self.status_combo = StyledCombobox(form_frame, textvariable=self.status_var, values=status_display, state="readonly")
        self.status_combo.pack(fill="x", pady=(5, 15))
        
        # Assigned Lawyer
        StyledLabel(form_frame, text=i18n.get('assigned_lawyer')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.lawyer_var = tk.StringVar()
        self.lawyer_combo = StyledCombobox(form_frame, textvariable=self.lawyer_var, state="readonly")
        self.lawyer_combo.pack(fill="x", pady=(5, 15))
        
        # Start Date
        StyledLabel(form_frame, text=i18n.get('start_date')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.start_date_picker = DatePicker(form_frame)
        self.start_date_picker.pack(fill="x", pady=(5, 15))
        
        # End Date
        StyledLabel(form_frame, text=i18n.get('end_date')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.end_date_picker = DatePicker(form_frame)
        self.end_date_picker.pack(fill="x", pady=(5, 15))
        
        # Description
        StyledLabel(form_frame, text=i18n.get('description')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.description_text = StyledText(form_frame, height=5)
        self.description_text.pack(fill="x", pady=(5, 15))
        
        # Buttons
        buttons_frame = tk.Frame(form_frame, bg="white")
        buttons_frame.pack(fill="x", pady=20)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('save'),
            command=self.save_case,
            style="success"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('cancel'),
            command=self.dialog.destroy,
            style="secondary"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
    
    def load_data(self):
        """Load clients and lawyers data"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Load clients
                cursor.execute("SELECT id, name FROM clients ORDER BY name")
                self.clients = cursor.fetchall()
                client_names = [RTLWidget.format_text(client['name']) for client in self.clients]
                self.client_combo['values'] = client_names
                
                # Load lawyers
                cursor.execute("SELECT id, full_name FROM users WHERE role IN ('lawyer', 'admin') AND is_active = 1 ORDER BY full_name")
                self.lawyers = cursor.fetchall()
                lawyer_names = [RTLWidget.format_text(lawyer['full_name']) for lawyer in self.lawyers]
                self.lawyer_combo['values'] = lawyer_names
                
        except Exception as e:
            show_error(f"Error loading data: {str(e)}")
    
    def load_case_data(self):
        """Load existing case data for editing"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT c.*, cl.name as client_name, u.full_name as lawyer_name
                    FROM cases c
                    LEFT JOIN clients cl ON c.client_id = cl.id
                    LEFT JOIN users u ON c.assigned_lawyer_id = u.id
                    WHERE c.id = ?
                ''', (self.case_id,))
                
                case = cursor.fetchone()
                if case:
                    self.case_number_var.set(case['case_number'] or '')
                    self.title_var.set(case['title'] or '')
                    self.court_var.set(case['court_name'] or '')
                    self.case_type_var.set(case['case_type'] or '')
                    self.opponent_var.set(case['opponent_name'] or '')
                    
                    # Set status
                    status_map = {'open': i18n.get('open'), 'closed': i18n.get('closed'), 
                                'pending': i18n.get('pending'), 'postponed': i18n.get('postponed')}
                    self.status_var.set(status_map.get(case['status'], case['status']))
                    
                    # Set client
                    if case['client_name']:
                        self.client_var.set(RTLWidget.format_text(case['client_name']))
                    
                    # Set lawyer
                    if case['lawyer_name']:
                        self.lawyer_var.set(RTLWidget.format_text(case['lawyer_name']))
                    
                    # Set dates
                    if case['start_date']:
                        try:
                            start_date = datetime.strptime(case['start_date'], "%Y-%m-%d").date()
                            self.start_date_picker.set_date(start_date)
                        except:
                            pass
                    
                    if case['end_date']:
                        try:
                            end_date = datetime.strptime(case['end_date'], "%Y-%m-%d").date()
                            self.end_date_picker.set_date(end_date)
                        except:
                            pass
                    
                    # Set description
                    if case['description']:
                        self.description_text.insert("1.0", case['description'])
                
        except Exception as e:
            show_error(f"Error loading case data: {str(e)}")
    
    def save_case(self):
        """Save case data"""
        try:
            # Validate required fields
            if not self.case_number_var.get().strip():
                show_error(i18n.get('case_number_required', 'Case number is required'))
                return
            
            if not self.title_var.get().strip():
                show_error(i18n.get('case_title_required', 'Case title is required'))
                return
            
            # Get client ID
            client_id = None
            client_name = self.client_var.get()
            for client in self.clients:
                if RTLWidget.format_text(client['name']) == client_name:
                    client_id = client['id']
                    break
            
            if not client_id:
                show_error(i18n.get('client_required', 'Please select a client'))
                return
            
            # Get lawyer ID
            lawyer_id = None
            lawyer_name = self.lawyer_var.get()
            for lawyer in self.lawyers:
                if RTLWidget.format_text(lawyer['full_name']) == lawyer_name:
                    lawyer_id = lawyer['id']
                    break
            
            # Get status value
            status_map = {i18n.get('open'): 'open', i18n.get('closed'): 'closed', 
                         i18n.get('pending'): 'pending', i18n.get('postponed'): 'postponed'}
            status = None
            for key, value in status_map.items():
                if key == self.status_var.get():
                    status = value
                    break
            if not status:
                status = 'open'
            
            # Get dates
            start_date = self.start_date_picker.get_date()
            end_date = self.end_date_picker.get_date()
            
            # Get description
            description = self.description_text.get("1.0", "end-1c").strip()
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.case_id:
                    # Update existing case
                    cursor.execute('''
                        UPDATE cases SET
                            case_number = ?, title = ?, client_id = ?, court_name = ?,
                            case_type = ?, opponent_name = ?, status = ?, assigned_lawyer_id = ?,
                            start_date = ?, end_date = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (
                        self.case_number_var.get().strip(),
                        self.title_var.get().strip(),
                        client_id,
                        self.court_var.get().strip(),
                        self.case_type_var.get().strip(),
                        self.opponent_var.get().strip(),
                        status,
                        lawyer_id,
                        start_date.strftime("%Y-%m-%d") if start_date else None,
                        end_date.strftime("%Y-%m-%d") if end_date else None,
                        description if description else None,
                        self.case_id
                    ))
                    message = i18n.get('case_updated', 'Case updated successfully')
                else:
                    # Insert new case
                    cursor.execute('''
                        INSERT INTO cases (
                            case_number, title, client_id, court_name, case_type,
                            opponent_name, status, assigned_lawyer_id, start_date,
                            end_date, description, created_by
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        self.case_number_var.get().strip(),
                        self.title_var.get().strip(),
                        client_id,
                        self.court_var.get().strip(),
                        self.case_type_var.get().strip(),
                        self.opponent_var.get().strip(),
                        status,
                        lawyer_id,
                        start_date.strftime("%Y-%m-%d") if start_date else None,
                        end_date.strftime("%Y-%m-%d") if end_date else None,
                        description if description else None,
                        auth.get_current_user()['id']
                    ))
                    message = i18n.get('case_added', 'Case added successfully')
                
                conn.commit()
                show_success(message)
                
                if self.callback:
                    self.callback()
                
                self.dialog.destroy()
                
        except Exception as e:
            show_error(f"Error saving case: {str(e)}")