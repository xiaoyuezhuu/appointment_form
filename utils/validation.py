import re
from datetime import datetime, timedelta, time
import validators

def validate_name(name):
    """Validate that the name is not empty and contains only letters."""
    if not name or not name.strip():
        return False, "Name cannot be empty."
    if not re.match(r'^[A-Za-z\s\-\'\.]+$', name):
        return False, "Name should only contain letters, spaces, hyphens, apostrophes, and periods."
    return True, ""

def validate_email(email):
    """Validate email format."""
    if not email or not email.strip():
        return False, "Email cannot be empty."
    if not validators.email(email):
        return False, "Invalid email format."
    return True, ""

def validate_phone(phone):
    """Validate phone number format."""
    if not phone or not phone.strip():
        return False, "Phone number cannot be empty."
    # Basic phone validation - can be customized for specific formats
    phone_clean = re.sub(r'[\s\-\(\)]+', '', phone)
    if not re.match(r'^\+?[\d]{10,15}$', phone_clean):
        return False, "Invalid phone number format."
    return True, ""

def validate_appointment_date(date_str, time_str):
    """Validate that the appointment date and time are in the future."""
    try:
        # Convert date string to datetime object
        date_format = "%Y-%m-%d"
        time_format = "%H:%M"
        
        selected_date = datetime.strptime(date_str, date_format).date()
        current_date = datetime.now().date()
        
        # For today's date, we need to check that the time isn't in the past
        if selected_date == current_date:
            selected_time = datetime.strptime(time_str, time_format).time()
            current_time = datetime.now().time()
            
            # Allow a 15-minute buffer for scheduling (no last-second appointments)
            buffer_minutes = 15
            current_time_with_buffer = (datetime.combine(current_date, current_time) + 
                                        timedelta(minutes=buffer_minutes)).time()
            
            if selected_time < current_time_with_buffer:
                return False, f"For today's appointments, please select a time at least {buffer_minutes} minutes in the future."
                
        # Check if date is too far in the future (e.g., 3 months)
        max_future_date = current_date + timedelta(days=90)
        if selected_date > max_future_date:
            return False, "Appointment date cannot be more than 3 months in the future."
            
        return True, ""
    except ValueError as e:
        return False, f"Invalid date or time format: {str(e)}"

def validate_appointment_type(appointment_type, valid_types):
    """Validate that the appointment type is in the list of valid types."""
    if not appointment_type or appointment_type not in valid_types:
        return False, "Please select a valid appointment type."
    return True, "" 