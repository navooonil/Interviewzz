from datetime import datetime

# Introduction to Utility Functions:
# Utility functions are generic helper functions used throughout the application.
# They are not tied to specific business logic (services) or API logic (routes).

def format_date(dt: datetime) -> str:
    """Format a datetime object to a user-friendly string."""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def log_debug_message(message: str):
    """Simple debugging utility (just prints to console for now)."""
    print(f"[DEBUG]: {message}")
