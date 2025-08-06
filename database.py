"""
Database models and management for Law Office Management System
"""
import sqlite3
import hashlib
import os
from datetime import datetime
from config import DB_PATH, DATA_DIR
import bcrypt

class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
    
    def init_database(self):
        """Initialize database with all required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('admin', 'lawyer', 'secretary')),
                    email TEXT,
                    phone TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Clients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    national_id TEXT UNIQUE,
                    address TEXT,
                    notes TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Cases table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_number TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    client_id INTEGER NOT NULL,
                    court_name TEXT,
                    case_type TEXT,
                    opponent_name TEXT,
                    status TEXT CHECK (status IN ('open', 'closed', 'pending', 'postponed')) DEFAULT 'open',
                    assigned_lawyer_id INTEGER,
                    start_date DATE,
                    end_date DATE,
                    description TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (assigned_lawyer_id) REFERENCES users (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    case_id INTEGER,
                    client_id INTEGER,
                    assigned_to INTEGER,
                    priority TEXT CHECK (priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
                    status TEXT CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')) DEFAULT 'pending',
                    due_date DATE,
                    reminder_date DATE,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_id) REFERENCES cases (id),
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (assigned_to) REFERENCES users (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    case_id INTEGER,
                    client_id INTEGER,
                    appointment_date DATETIME NOT NULL,
                    duration INTEGER DEFAULT 60,
                    location TEXT,
                    attendees TEXT,
                    status TEXT CHECK (status IN ('scheduled', 'completed', 'cancelled', 'rescheduled')) DEFAULT 'scheduled',
                    reminder_sent BOOLEAN DEFAULT 0,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_id) REFERENCES cases (id),
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Documents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    file_type TEXT,
                    case_id INTEGER,
                    client_id INTEGER,
                    title TEXT,
                    description TEXT,
                    tags TEXT,
                    uploaded_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_id) REFERENCES cases (id),
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (uploaded_by) REFERENCES users (id)
                )
            ''')
            
            # Invoices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE NOT NULL,
                    client_id INTEGER NOT NULL,
                    case_id INTEGER,
                    amount DECIMAL(10,2) NOT NULL,
                    tax_amount DECIMAL(10,2) DEFAULT 0,
                    total_amount DECIMAL(10,2) NOT NULL,
                    description TEXT,
                    issue_date DATE NOT NULL,
                    due_date DATE,
                    status TEXT CHECK (status IN ('draft', 'sent', 'paid', 'overdue', 'cancelled')) DEFAULT 'draft',
                    payment_date DATE,
                    payment_method TEXT,
                    notes TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (case_id) REFERENCES cases (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Case sessions/hearings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS case_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER NOT NULL,
                    session_date DATETIME NOT NULL,
                    court_name TEXT,
                    session_type TEXT,
                    status TEXT CHECK (status IN ('scheduled', 'completed', 'postponed', 'cancelled')) DEFAULT 'scheduled',
                    notes TEXT,
                    next_session_date DATETIME,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_id) REFERENCES cases (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    description TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            # Create default admin user if no users exist
            self.create_default_admin()
    
    def create_default_admin(self):
        """Create default admin user if no users exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                # Create default admin user
                password = "admin123"
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, role, email)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("admin", password_hash, "System Administrator", "admin", "admin@lawoffice.com"))
                
                conn.commit()
                print("Default admin user created: username=admin, password=admin123")
    
    def backup_database(self, backup_path=None):
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"law_office_backup_{timestamp}.db"
            backup_path = os.path.join(os.path.dirname(__file__), "data", "backups", backup_filename)
        
        try:
            # Copy database file
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Backup failed: {e}")
            return None
    
    def restore_database(self, backup_path):
        """Restore database from backup"""
        try:
            import shutil
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False

# Global database instance
db = DatabaseManager()