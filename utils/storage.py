import os
import pandas as pd
from datetime import datetime

# Define the path to the appointments CSV file
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
APPOINTMENTS_FILE = os.path.join(DATA_DIR, 'appointments.csv')

def initialize_storage():
    """Create the appointments CSV file if it doesn't exist."""
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(DATA_DIR, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Check if the appointments file exists
    if not os.path.exists(APPOINTMENTS_FILE):
        # Create an empty DataFrame with the desired columns
        columns = [
            'id', 'name', 'email', 'phone', 'appointment_type', 
            'appointment_date', 'appointment_time', 'reason', 'notes', 
            'file_uploaded', 'file_name', 'file_path',
            'created_at', 'status'
        ]
        df = pd.DataFrame(columns=columns)
        # Save the empty DataFrame to CSV
        df.to_csv(APPOINTMENTS_FILE, index=False)
        return True
    return False

def save_appointment(appointment_data):
    """Save a new appointment to the CSV file."""
    # Initialize storage if needed
    initialize_storage()
    
    try:
        # Read existing appointments
        appointments_df = pd.read_csv(APPOINTMENTS_FILE)
        
        # Generate a unique ID based on timestamp
        appointment_id = int(datetime.now().timestamp())
        
        # Add ID, created timestamp, and initial status
        appointment_data['id'] = appointment_id
        appointment_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        appointment_data['status'] = 'pending'
        
        # Ensure all required columns exist in the data
        if 'file_uploaded' not in appointment_data:
            appointment_data['file_uploaded'] = False
        if 'file_name' not in appointment_data:
            appointment_data['file_name'] = ''
        if 'file_path' not in appointment_data:
            appointment_data['file_path'] = ''
        
        # Append new appointment as a DataFrame
        new_appointment_df = pd.DataFrame([appointment_data])
        updated_df = pd.concat([appointments_df, new_appointment_df], ignore_index=True)
        
        # Save to CSV
        updated_df.to_csv(APPOINTMENTS_FILE, index=False)
        return True, appointment_id
    except Exception as e:
        return False, str(e)

def get_all_appointments():
    """Retrieve all appointments from the CSV file."""
    # Initialize storage if needed
    initialize_storage()
    
    try:
        # Read appointments from CSV
        appointments_df = pd.read_csv(APPOINTMENTS_FILE)
        return True, appointments_df
    except Exception as e:
        return False, str(e)

def get_appointment_by_id(appointment_id):
    """Retrieve a specific appointment by ID."""
    # Initialize storage if needed
    initialize_storage()
    
    try:
        # Read appointments from CSV
        appointments_df = pd.read_csv(APPOINTMENTS_FILE)
        
        # Filter by appointment ID
        appointment = appointments_df[appointments_df['id'] == int(appointment_id)]
        
        if appointment.empty:
            return False, "Appointment not found"
        
        return True, appointment.iloc[0].to_dict()
    except Exception as e:
        return False, str(e)

def update_appointment_status(appointment_id, new_status):
    """Update the status of an appointment."""
    # Initialize storage if needed
    initialize_storage()
    
    try:
        # Read appointments from CSV
        appointments_df = pd.read_csv(APPOINTMENTS_FILE)
        
        # Find the appointment by ID
        mask = appointments_df['id'] == int(appointment_id)
        
        if not any(mask):
            return False, "Appointment not found"
        
        # Update the status
        appointments_df.loc[mask, 'status'] = new_status
        
        # Save to CSV
        appointments_df.to_csv(APPOINTMENTS_FILE, index=False)
        return True, "Status updated successfully"
    except Exception as e:
        return False, str(e) 