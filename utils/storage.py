import os
import pandas as pd
from datetime import datetime
from utils.db_connection import (
    initialize_database,
    get_appointments_table,
    appointment_to_dict,
    test_connection,
    save_file_to_supabase
)
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Define bucket names from environment variables or use defaults
UPLOAD_BUCKET = os.getenv("UPLOAD_BUCKET", "uploads")
THIRST_TRAP_BUCKET = os.getenv("THIRST_TRAP_BUCKET", "thirst_traps")

def initialize_storage():
    """Initialize Supabase tables and storage."""
    # Initialize database
    try:
        initialize_database()
        return True
    except Exception as e:
        print(f"Error initializing Supabase: {e}")
        return False

def save_appointment(appointment_data):
    """Save a new appointment to Supabase and handle file uploads."""
    try:
        # Handle file upload if exists
        if appointment_data.get('file_uploaded', False) and 'uploaded_file' in appointment_data:
            uploaded_file = appointment_data['uploaded_file']
            
            try:
                # Upload file to Supabase storage
                file_path = save_file_to_supabase(
                    uploaded_file.getvalue(),
                    uploaded_file.name,
                    UPLOAD_BUCKET
                )
                
                # Update file info in appointment data
                appointment_data['file_name'] = uploaded_file.name
                appointment_data['file_path'] = file_path
            except Exception as e:
                print(f"Error uploading file to Supabase: {e}")
                appointment_data['file_uploaded'] = False
                appointment_data['file_name'] = ''
                appointment_data['file_path'] = ''
        
        # Handle thirst trap upload for interns
        if appointment_data.get('is_intern', False) and appointment_data.get('thirst_trap_uploaded', False) and 'thirst_trap_file' in appointment_data:
            thirst_trap_file = appointment_data['thirst_trap_file']
            
            try:
                print(f"Attempting to upload thirst trap: {thirst_trap_file.name}")
                print(f"Uploading to bucket: {THIRST_TRAP_BUCKET}")
                
                # Upload thirst trap to Supabase storage
                thirst_trap_path = save_file_to_supabase(
                    thirst_trap_file.getvalue(),
                    thirst_trap_file.name,
                    THIRST_TRAP_BUCKET
                )
                
                print(f"Thirst trap uploaded successfully. URL: {thirst_trap_path}")
                
                # Update thirst trap info in appointment data
                appointment_data['thirst_trap_filename'] = thirst_trap_file.name
                appointment_data['thirst_trap_path'] = thirst_trap_path
            except Exception as e:
                error_message = f"Error uploading thirst trap to Supabase: {e}"
                print(error_message)
                import traceback
                traceback.print_exc()
                appointment_data['thirst_trap_uploaded'] = False
                appointment_data['thirst_trap_filename'] = ''
                appointment_data['thirst_trap_path'] = ''
                raise Exception(error_message)
        
        # Remove the file objects before saving to database (they can't be serialized)
        if 'uploaded_file' in appointment_data:
            del appointment_data['uploaded_file']
        if 'thirst_trap_file' in appointment_data:
            del appointment_data['thirst_trap_file']
        
        # Add created_at and status if not present
        if 'created_at' not in appointment_data:
            appointment_data['created_at'] = datetime.now().isoformat()
        if 'status' not in appointment_data:
            appointment_data['status'] = 'pending'
            
        # Add a unique ID if not present - using timestamp instead of UUID for bigint compatibility
        if 'id' not in appointment_data:
            # Use timestamp as integer ID instead of UUID since the column is bigint
            appointment_data['id'] = int(datetime.now().timestamp() * 1000)  # milliseconds for uniqueness
        
        # Insert into Supabase
        result = get_appointments_table().insert(appointment_data).execute()
        
        # Get the ID of the newly created appointment
        appointment_id = appointment_data['id']
        
        return True, appointment_id
    except Exception as e:
        return False, str(e)

def get_all_appointments():
    """Retrieve all appointments from Supabase."""
    try:
        # Query all appointments
        result = get_appointments_table().select('*').execute()
        
        # Extract data
        appointments_data = result.data
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(appointments_data)
        
        return True, df
    except Exception as e:
        return False, str(e)

def get_appointment_by_id(appointment_id):
    """Retrieve a specific appointment by ID."""
    try:
        # Query the appointment by ID
        result = get_appointments_table().select('*').eq('id', appointment_id).execute()
        
        # Check if appointment was found
        if not result.data:
            return False, "Appointment not found"
        
        # Return the first match
        return True, result.data[0]
    except Exception as e:
        return False, str(e)

def update_appointment_status(appointment_id, new_status):
    """Update the status of an appointment."""
    try:
        # Update the status
        result = get_appointments_table().update({"status": new_status}).eq('id', appointment_id).execute()
        
        # Check if any rows were affected
        if not result.data:
            return False, "Appointment not found"
        
        return True, "Status updated successfully"
    except Exception as e:
        return False, str(e)

def check_database_connection():
    """Test the Supabase connection and return the result."""
    return test_connection() 