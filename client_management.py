"""
Client Management Module for Law Office Management System
"""
import tkinter as tk
from tkinter import ttk
from gui_components import *
from database import db
from auth import auth
from i18n import i18n

class ClientManagement:
    def __init__(self, parent):
        self.parent = parent
        self.current_client = None
        self.create_interface()
        self.load_clients()
    
    def create_interface(self):
        """Create the client management interface"""
        # Main frame
        main_frame = tk.Frame(self.parent, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 20))
        
        StyledLabel(header_frame, text=i18n.get('client_management'), style="title").pack(
            side="right" if i18n.is_rtl() else "left"
        )
        
        # Buttons frame
        buttons_frame = tk.Frame(header_frame, bg="white")
        buttons_frame.pack(side="left" if i18n.is_rtl() else "right")
        
        StyledButton(
            buttons_frame,
            text=i18n.get('add_client'),
            command=self.add_client,
            style="success"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('edit'),
            command=self.edit_client,
            style="primary"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('delete'),
            command=self.delete_client,
            style="danger"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('view_cases', 'View Cases'),
            command=self.view_client_cases,
            style="secondary"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('refresh'),
            command=self.load_clients,
            style="secondary"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        # Search frame
        search_frame = SearchFrame(main_frame, self.search_clients)
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Clients list
        list_frame = tk.Frame(main_frame, bg="white")
        list_frame.pack(fill="both", expand=True)
        
        # Create treeview for clients
        columns = (
            i18n.get('client_name'),
            i18n.get('phone'),
            i18n.get('email'),
            i18n.get('national_id'),
            i18n.get('total_cases', 'Total Cases'),
            i18n.get('created_at', 'Created Date')
        )
        
        self.clients_tree = DataTreeview(list_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.clients_tree.heading(col, text=RTLWidget.format_text(col))
            self.clients_tree.column(col, width=150, anchor="center")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.clients_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.clients_tree.xview)
        
        self.clients_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.clients_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click to edit
        self.clients_tree.bind('<Double-1>', lambda e: self.edit_client())
        
        # Bind selection
        self.clients_tree.bind('<<TreeviewSelect>>', self.on_client_select)
    
    def load_clients(self):
        """Load clients from database"""
        try:
            # Clear existing items
            for item in self.clients_tree.get_children():
                self.clients_tree.delete(item)
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get clients with case count
                query = '''
                    SELECT 
                        c.id,
                        c.name,
                        c.phone,
                        c.email,
                        c.national_id,
                        c.created_at,
                        COUNT(cs.id) as case_count
                    FROM clients c
                    LEFT JOIN cases cs ON c.id = cs.client_id
                    GROUP BY c.id, c.name, c.phone, c.email, c.national_id, c.created_at
                    ORDER BY c.created_at DESC
                '''
                
                cursor.execute(query)
                clients = cursor.fetchall()
                
                for client in clients:
                    # Format data for display
                    client_data = [
                        client['name'] or '',
                        client['phone'] or '',
                        client['email'] or '',
                        client['national_id'] or '',
                        str(client['case_count']) if client['case_count'] else '0',
                        self.format_date(client['created_at']) if client['created_at'] else ''
                    ]
                    
                    # Insert with RTL formatting
                    formatted_data = [RTLWidget.format_text(str(val)) for val in client_data]
                    item = self.clients_tree.insert("", "end", values=formatted_data)
                    
                    # Store client ID in item tags
                    self.clients_tree.set(item, '#1', client['id'])
                    
        except Exception as e:
            show_error(f"Error loading clients: {str(e)}")
    
    def search_clients(self, search_term):
        """Search clients"""
        if not search_term.strip():
            self.load_clients()
            return
        
        try:
            # Clear existing items
            for item in self.clients_tree.get_children():
                self.clients_tree.delete(item)
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                search_pattern = f"%{search_term}%"
                query = '''
                    SELECT 
                        c.id,
                        c.name,
                        c.phone,
                        c.email,
                        c.national_id,
                        c.created_at,
                        COUNT(cs.id) as case_count
                    FROM clients c
                    LEFT JOIN cases cs ON c.id = cs.client_id
                    WHERE c.name LIKE ? OR c.phone LIKE ? OR c.email LIKE ? OR c.national_id LIKE ?
                    GROUP BY c.id, c.name, c.phone, c.email, c.national_id, c.created_at
                    ORDER BY c.created_at DESC
                '''
                
                cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
                clients = cursor.fetchall()
                
                for client in clients:
                    client_data = [
                        client['name'] or '',
                        client['phone'] or '',
                        client['email'] or '',
                        client['national_id'] or '',
                        str(client['case_count']) if client['case_count'] else '0',
                        self.format_date(client['created_at']) if client['created_at'] else ''
                    ]
                    
                    formatted_data = [RTLWidget.format_text(str(val)) for val in client_data]
                    item = self.clients_tree.insert("", "end", values=formatted_data)
                    self.clients_tree.set(item, '#1', client['id'])
                    
        except Exception as e:
            show_error(f"Error searching clients: {str(e)}")
    
    def on_client_select(self, event):
        """Handle client selection"""
        selection = self.clients_tree.selection()
        if selection:
            item = selection[0]
            # Get client ID from database based on client name
            values = self.clients_tree.item(item)['values']
            if values:
                client_name = values[0]
                try:
                    with db.get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM clients WHERE name = ?", (client_name,))
                        result = cursor.fetchone()
                        if result:
                            self.current_client = result['id']
                        else:
                            self.current_client = None
                except:
                    self.current_client = None
    
    def add_client(self):
        """Add new client"""
        ClientDialog(self.parent, callback=self.load_clients)
    
    def edit_client(self):
        """Edit selected client"""
        if not self.current_client:
            show_warning(i18n.get('select_client_first', 'Please select a client first'))
            return
        
        ClientDialog(self.parent, client_id=self.current_client, callback=self.load_clients)
    
    def delete_client(self):
        """Delete selected client"""
        if not self.current_client:
            show_warning(i18n.get('select_client_first', 'Please select a client first'))
            return
        
        try:
            # Check if client has associated cases
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cases WHERE client_id = ?", (self.current_client,))
                case_count = cursor.fetchone()[0]
                
                if case_count > 0:
                    show_warning(i18n.get('cannot_delete_client_with_cases', 'Cannot delete client with associated cases'))
                    return
            
            if not confirm_action(i18n.get('confirm_delete_client', 'Are you sure you want to delete this client?')):
                return
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clients WHERE id = ?", (self.current_client,))
                conn.commit()
            
            show_success(i18n.get('client_deleted', 'Client deleted successfully'))
            self.load_clients()
            
        except Exception as e:
            show_error(f"Error deleting client: {str(e)}")
    
    def view_client_cases(self):
        """View cases for selected client"""
        if not self.current_client:
            show_warning(i18n.get('select_client_first', 'Please select a client first'))
            return
        
        ClientCasesDialog(self.parent, self.current_client)
    
    def format_date(self, date_str):
        """Format date for display"""
        if not date_str:
            return ""
        
        try:
            from datetime import datetime
            if isinstance(date_str, str):
                parsed_date = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
            else:
                parsed_date = date_str
            
            return parsed_date.strftime("%d/%m/%Y")
        except:
            return str(date_str)

class ClientDialog:
    def __init__(self, parent, client_id=None, callback=None):
        self.parent = parent
        self.client_id = client_id
        self.callback = callback
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(RTLWidget.format_text(i18n.get('edit_client') if client_id else i18n.get('add_client')))
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (250)
        y = (self.dialog.winfo_screenheight() // 2) - (300)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        self.create_form()
        
        if client_id:
            self.load_client_data()
    
    def create_form(self):
        """Create client form"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Client Name
        StyledLabel(main_frame, text=f"{i18n.get('client_name')} *").pack(anchor="e" if i18n.is_rtl() else "w")
        self.name_var = tk.StringVar()
        StyledEntry(main_frame, textvariable=self.name_var).pack(fill="x", pady=(5, 15))
        
        # Phone
        StyledLabel(main_frame, text=i18n.get('phone')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.phone_var = tk.StringVar()
        StyledEntry(main_frame, textvariable=self.phone_var).pack(fill="x", pady=(5, 15))
        
        # Email
        StyledLabel(main_frame, text=i18n.get('email')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.email_var = tk.StringVar()
        StyledEntry(main_frame, textvariable=self.email_var).pack(fill="x", pady=(5, 15))
        
        # National ID
        StyledLabel(main_frame, text=i18n.get('national_id')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.national_id_var = tk.StringVar()
        StyledEntry(main_frame, textvariable=self.national_id_var).pack(fill="x", pady=(5, 15))
        
        # Address
        StyledLabel(main_frame, text=i18n.get('address')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.address_text = StyledText(main_frame, height=5)
        self.address_text.pack(fill="x", pady=(5, 15))
        
        # Notes
        StyledLabel(main_frame, text=i18n.get('notes')).pack(anchor="e" if i18n.is_rtl() else "w")
        self.notes_text = StyledText(main_frame, height=5)
        self.notes_text.pack(fill="x", pady=(5, 15))
        
        # Required field note
        StyledLabel(main_frame, text="* " + i18n.get('required_field'), fg="#888").pack(anchor="e" if i18n.is_rtl() else "w", pady=(5, 15))
        
        # Buttons
        buttons_frame = tk.Frame(main_frame, bg="white")
        buttons_frame.pack(fill="x", pady=20)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('save'),
            command=self.save_client,
            style="success"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
        
        StyledButton(
            buttons_frame,
            text=i18n.get('cancel'),
            command=self.dialog.destroy,
            style="secondary"
        ).pack(side="right" if i18n.is_rtl() else "left", padx=5)
    
    def load_client_data(self):
        """Load existing client data for editing"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM clients WHERE id = ?", (self.client_id,))
                client = cursor.fetchone()
                
                if client:
                    self.name_var.set(client['name'] or '')
                    self.phone_var.set(client['phone'] or '')
                    self.email_var.set(client['email'] or '')
                    self.national_id_var.set(client['national_id'] or '')
                    
                    if client['address']:
                        self.address_text.insert("1.0", client['address'])
                    
                    if client['notes']:
                        self.notes_text.insert("1.0", client['notes'])
                
        except Exception as e:
            show_error(f"Error loading client data: {str(e)}")
    
    def save_client(self):
        """Save client data"""
        try:
            # Validate required fields
            if not self.name_var.get().strip():
                show_error(i18n.get('client_name_required', 'Client name is required'))
                return
            
            # Get text data
            address = self.address_text.get("1.0", "end-1c").strip()
            notes = self.notes_text.get("1.0", "end-1c").strip()
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.client_id:
                    # Update existing client
                    cursor.execute('''
                        UPDATE clients SET
                            name = ?, phone = ?, email = ?, national_id = ?,
                            address = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (
                        self.name_var.get().strip(),
                        self.phone_var.get().strip() if self.phone_var.get().strip() else None,
                        self.email_var.get().strip() if self.email_var.get().strip() else None,
                        self.national_id_var.get().strip() if self.national_id_var.get().strip() else None,
                        address if address else None,
                        notes if notes else None,
                        self.client_id
                    ))
                    message = i18n.get('client_updated', 'Client updated successfully')
                else:
                    # Insert new client
                    cursor.execute('''
                        INSERT INTO clients (name, phone, email, national_id, address, notes, created_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        self.name_var.get().strip(),
                        self.phone_var.get().strip() if self.phone_var.get().strip() else None,
                        self.email_var.get().strip() if self.email_var.get().strip() else None,
                        self.national_id_var.get().strip() if self.national_id_var.get().strip() else None,
                        address if address else None,
                        notes if notes else None,
                        auth.get_current_user()['id']
                    ))
                    message = i18n.get('client_added', 'Client added successfully')
                
                conn.commit()
                show_success(message)
                
                if self.callback:
                    self.callback()
                
                self.dialog.destroy()
                
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                show_error(i18n.get('client_exists', 'Client with this national ID already exists'))
            else:
                show_error(f"Error saving client: {str(e)}")

class ClientCasesDialog:
    def __init__(self, parent, client_id):
        self.parent = parent
        self.client_id = client_id
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(RTLWidget.format_text(i18n.get('client_cases', 'Client Cases')))
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400)
        y = (self.dialog.winfo_screenheight() // 2) - (300)
        self.dialog.geometry(f"800x600+{x}+{y}")
        
        self.create_interface()
        self.load_client_info()
        self.load_cases()
    
    def create_interface(self):
        """Create the interface"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Client info frame
        info_frame = tk.Frame(main_frame, bg="white")
        info_frame.pack(fill="x", pady=(0, 20))
        
        self.client_info_label = StyledLabel(info_frame, text="", style="header")
        self.client_info_label.pack(anchor="e" if i18n.is_rtl() else "w")
        
        # Cases list
        StyledLabel(main_frame, text=i18n.get('cases'), style="header").pack(anchor="e" if i18n.is_rtl() else "w", pady=(0, 10))
        
        list_frame = tk.Frame(main_frame, bg="white")
        list_frame.pack(fill="both", expand=True)
        
        # Create treeview for cases
        columns = (
            i18n.get('case_number'),
            i18n.get('case_title'),
            i18n.get('case_type'),
            i18n.get('case_status'),
            i18n.get('start_date')
        )
        
        self.cases_tree = DataTreeview(list_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.cases_tree.heading(col, text=RTLWidget.format_text(col))
            self.cases_tree.column(col, width=150, anchor="center")
        
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
        
        # Close button
        close_button = StyledButton(
            main_frame,
            text=i18n.get('close'),
            command=self.dialog.destroy,
            style="secondary"
        )
        close_button.pack(pady=20)
    
    def load_client_info(self):
        """Load client information"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, phone, email FROM clients WHERE id = ?", (self.client_id,))
                client = cursor.fetchone()
                
                if client:
                    info_text = f"{i18n.get('client_name')}: {client['name']}"
                    if client['phone']:
                        info_text += f" | {i18n.get('phone')}: {client['phone']}"
                    if client['email']:
                        info_text += f" | {i18n.get('email')}: {client['email']}"
                    
                    self.client_info_label.config(text=RTLWidget.format_text(info_text))
                
        except Exception as e:
            show_error(f"Error loading client info: {str(e)}")
    
    def load_cases(self):
        """Load client cases"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT case_number, title, case_type, status, start_date
                    FROM cases 
                    WHERE client_id = ?
                    ORDER BY created_at DESC
                ''', (self.client_id,))
                
                cases = cursor.fetchall()
                
                for case in cases:
                    case_data = [
                        case['case_number'] or '',
                        case['title'] or '',
                        case['case_type'] or '',
                        i18n.get(case['status'], case['status']) if case['status'] else '',
                        self.format_date(case['start_date']) if case['start_date'] else ''
                    ]
                    
                    formatted_data = [RTLWidget.format_text(str(val)) for val in case_data]
                    self.cases_tree.insert("", "end", values=formatted_data)
                
        except Exception as e:
            show_error(f"Error loading cases: {str(e)}")
    
    def format_date(self, date_str):
        """Format date for display"""
        if not date_str:
            return ""
        
        try:
            from datetime import datetime
            if isinstance(date_str, str):
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                parsed_date = date_str
            
            return parsed_date.strftime("%d/%m/%Y")
        except:
            return str(date_str)