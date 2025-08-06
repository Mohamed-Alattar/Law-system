"""
User authentication and role management
"""
import bcrypt
from datetime import datetime
from database import db

class AuthManager:
    def __init__(self):
        self.current_user = None
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, password_hash, full_name, role, email, phone, is_active
                    FROM users 
                    WHERE username = ? AND is_active = 1
                ''', (username,))
                
                user = cursor.fetchone()
                
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                    self.current_user = {
                        'id': user['id'],
                        'username': user['username'],
                        'full_name': user['full_name'],
                        'role': user['role'],
                        'email': user['email'],
                        'phone': user['phone']
                    }
                    return True
                
                return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def has_permission(self, required_role=None):
        """Check if current user has required permission"""
        if not self.is_authenticated():
            return False
        
        if required_role is None:
            return True
        
        user_role = self.current_user['role']
        
        # Role hierarchy: admin > lawyer > secretary
        role_hierarchy = {
            'admin': 3,
            'lawyer': 2,
            'secretary': 1
        }
        
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.is_authenticated() and self.current_user['role'] == 'admin'
    
    def is_lawyer(self):
        """Check if current user is lawyer or admin"""
        return self.has_permission('lawyer')
    
    def can_manage_users(self):
        """Check if current user can manage other users"""
        return self.is_admin()
    
    def can_manage_cases(self):
        """Check if current user can manage cases"""
        return self.has_permission('lawyer')
    
    def can_view_financial_reports(self):
        """Check if current user can view financial reports"""
        return self.has_permission('lawyer')

class UserManager:
    def __init__(self):
        pass
    
    def create_user(self, username, password, full_name, role, email=None, phone=None):
        """Create a new user"""
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, role, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, password_hash, full_name, role, email, phone))
                
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update_user(self, user_id, **kwargs):
        """Update user information"""
        try:
            # Build update query dynamically
            update_fields = []
            values = []
            
            allowed_fields = ['username', 'full_name', 'role', 'email', 'phone', 'is_active']
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    update_fields.append(f"{field} = ?")
                    values.append(value)
                elif field == 'password' and value:
                    # Hash new password
                    password_hash = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
                    update_fields.append("password_hash = ?")
                    values.append(password_hash)
            
            if not update_fields:
                return False
            
            # Add updated_at timestamp
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(user_id)
            
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, user_id):
        """Delete a user (soft delete by setting is_active = 0)"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user_id,))
                
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, full_name, role, email, phone, is_active, created_at
                    FROM users 
                    WHERE id = ?
                ''', (user_id,))
                
                return cursor.fetchone()
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, full_name, role, email, phone, is_active, created_at
                    FROM users 
                    WHERE username = ?
                ''', (username,))
                
                return cursor.fetchone()
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_all_users(self, active_only=True):
        """Get all users"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT id, username, full_name, role, email, phone, is_active, created_at
                    FROM users
                '''
                
                if active_only:
                    query += " WHERE is_active = 1"
                
                query += " ORDER BY full_name"
                
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_lawyers(self):
        """Get all lawyers (users with role 'lawyer' or 'admin')"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, full_name, role, email, phone
                    FROM users 
                    WHERE role IN ('lawyer', 'admin') AND is_active = 1
                    ORDER BY full_name
                ''')
                
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting lawyers: {e}")
            return []
    
    def validate_username(self, username, exclude_user_id=None):
        """Check if username is available"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT COUNT(*) FROM users WHERE username = ?"
                params = [username]
                
                if exclude_user_id:
                    query += " AND id != ?"
                    params.append(exclude_user_id)
                
                cursor.execute(query, params)
                count = cursor.fetchone()[0]
                
                return count == 0
        except Exception as e:
            print(f"Error validating username: {e}")
            return False

# Global instances
auth = AuthManager()
user_manager = UserManager()