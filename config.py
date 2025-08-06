"""
Configuration settings for Law Office Management System
"""
import os

# Application settings
APP_NAME = "Law Office Management System"
APP_VERSION = "1.0.0"
APP_TITLE = "نظام إدارة مكتب المحاماة - Law Office Management"

# Database settings
DB_NAME = "law_office.db"
DB_PATH = os.path.join(os.path.dirname(__file__), "data", DB_NAME)

# Directories
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
BACKUPS_DIR = os.path.join(DATA_DIR, "backups")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# Language settings
DEFAULT_LANGUAGE = "ar"  # Arabic by default
SUPPORTED_LANGUAGES = ["ar", "en"]

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FONT_FAMILY_AR = "Arial Unicode MS"
FONT_FAMILY_EN = "Arial"
FONT_SIZE_NORMAL = 12
FONT_SIZE_HEADER = 16
FONT_SIZE_TITLE = 20

# Colors
PRIMARY_COLOR = "#2C3E50"
SECONDARY_COLOR = "#3498DB"
SUCCESS_COLOR = "#27AE60"
WARNING_COLOR = "#F39C12"
DANGER_COLOR = "#E74C3C"
BACKGROUND_COLOR = "#ECF0F1"
TEXT_COLOR = "#2C3E50"

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"

# File upload settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.txt']

# Reminder settings
REMINDER_DAYS_BEFORE = [1, 3, 7]  # Days before deadline to show reminders

# Create necessary directories
for directory in [DATA_DIR, DOCUMENTS_DIR, BACKUPS_DIR, REPORTS_DIR]:
    os.makedirs(directory, exist_ok=True)