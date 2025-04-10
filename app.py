import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import pytz
from utils import validation, storage
import uuid
import re
from supabase import create_client, Client

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Page configuration
st.set_page_config(
    page_title="Xiaoyue's Appointment Form",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Constants
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes

# Define appointment types
APPOINTMENT_TYPES = [
    "Career Development",
    "Routine Check-up",
    "Urgent Care",
    "Performance Evaluation"
]

# Function to get the current date in user's local timezone
def get_local_date():
    # We'll use the client's browser time via a JavaScript function
    # This ensures we're using the user's local timezone
    return datetime.now().date()  # Fallback for initial load

# Enhanced CSS for better styling
st.markdown("""
<style>
    /* Import Google Fonts - Poppins is a stylish yet minimalistic font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Color scheme */
    :root {
        --primary-color: #4F6D7A;
        --secondary-color: #56A3A6;
        --accent-color: #F4A261;
        --background-color: #F8F9FA;
        --text-color: #2C3E50;
        --light-accent: #E3F2FD;
        --naughty-pink: #FF5A8C;
    }
    
    /* Base styling */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: var(--text-color);
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--accent-color);
    }
    
    h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        color: var(--primary-color);
    }
    
    /* Subheader styling */
    .subheader {
        font-size: 1.5rem;
        font-weight: 500;
        color: var(--secondary-color);
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Input fields styling */
    .stTextInput input, .stSelectbox, .stDateInput input, .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #E0E0E0;
        padding: 0.75rem;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stSelectbox:focus, .stDateInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(244, 162, 97, 0.2);
    }
    
    /* Button styling */
    .stButton button {
        background-color: var(--secondary-color) !important;
        color: white !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: 5px;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 100%;
        height: auto;
    }
    
    /* Naughty pink button styling */
    .stForm button[kind="formSubmit"], .stButton button[kind="primaryFormSubmit"] {
        background-color: var(--naughty-pink) !important;
    }
    
    .stButton button:hover {
        background-color: var(--primary-color) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    /* Naughty pink button hover styling */
    .stForm button[kind="formSubmit"]:hover, .stButton button[kind="primaryFormSubmit"]:hover {
        background-color: #FF3A7C !important;
    }
    
    /* Form sections */
    .form-section {
        background-color: var(--background-color);
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--secondary-color);
    }
    
    /* Success message styling */
    .success-message {
        background-color: #d1e7dd;
        color: #0f5132;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #0f5132;
        font-family: 'Poppins', sans-serif;
    }
    
    .success-message h3 {
        color: #0f5132;
        margin-top: 0;
    }
    
    /* Error message styling */
    .error-message {
        background-color: #f8d7da;
        color: #842029;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        border-left: 4px solid #842029;
    }
    
    /* Field label styling */
    label {
        font-weight: 500;
        color: var(--primary-color);
    }
    
    /* Required field indicator */
    .required-field::after {
        content: "*";
        color: #d32f2f;
        margin-left: 4px;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 1px dashed var(--secondary-color);
        border-radius: 5px;
        padding: 1rem;
        background-color: var(--light-accent);
    }
    
    /* Responsive styling */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .stButton button {
            padding: 0.5rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize storage and test database connection
    storage.initialize_storage()
    
    # Test database connection
    db_connection_success, db_message = storage.check_database_connection()
    if not db_connection_success:
        st.error(f"⚠️ Database Connection Error: {db_message}")
        st.warning("The application will continue to run, but appointments can't be saved to the database!")
    
    # App title with emoji for visual appeal
    st.markdown("<h1>Xiaoyue's Office Hours</h1>", unsafe_allow_html=True)
    
    # Create a unique form key using session state to prevent resubmission on refresh
    if 'form_key' not in st.session_state:
        st.session_state.form_key = 1
    
    # Show confirmation or continue with form
    if 'appointment_submitted' in st.session_state and st.session_state.appointment_submitted:
        show_confirmation()
    else:
        show_appointment_form()

def show_appointment_form():
    """Display the appointment booking form."""
    
    # Initialize session state for thirst trap if not present
    if 'thirst_trap' not in st.session_state:
        st.session_state.thirst_trap = False
    
    # Create the form
    with st.form(key=f'appointment_form_{st.session_state.form_key}'):
        # Personal Information Section with custom styling
        # st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<p class="subheader">👤 Your Information</p>', unsafe_allow_html=True)
        
        # Personal information
        name = st.text_input("Name*")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email Address*")
        with col2:
            phone = st.text_input("Phone Number*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Appointment Details Section
        # st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<p class="subheader">📅 Appointment Details</p>', unsafe_allow_html=True)
        
        # Appointment type
        appointment_type = st.selectbox(
            "Appointment Type*",
            options=["Select an appointment type"] + APPOINTMENT_TYPES
        )
        
        # Intern checkbox and conditional message
        col1, col2 = st.columns([3, 1])
        with col2:
            is_intern = st.checkbox("Are you an intern?")
            
        # Show message if intern is checked
        if is_intern:
            st.markdown("""
            <div style="background-color: #FF5A5F; color: white; padding: 20px; border-radius: 10px; margin: 10px 0; animation: pulse 1.5s infinite;">
                <h3 style="margin-top: 0; color: white;">🔥 Intern Application Notice 🔥</h3>
                <p style="font-size: 16px; margin-bottom: 0;">You must submit a thirst trap as part of the application process.</p>
            </div>
            <style>
                @keyframes pulse {
                    0% { opacity: 0.8; }
                    50% { opacity: 1; }
                    100% { opacity: 0.8; }
                }
            </style>
            """, unsafe_allow_html=True)
        
        # Date and time selection
        col1, col2 = st.columns(2)
        with col1:
            # Set min date to tomorrow and max date to 1 months from now
            min_date = get_local_date()
            max_date = min_date + timedelta(days=30)
            appointment_date = st.date_input(
                "Preferred Date*",
                min_value=min_date,
                max_value=max_date,
                value=min_date
            )
        
        with col2:
            appointment_time = st.selectbox(
                "Preferred Time*",
                options=[
                    "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                    "18:00", "19:00", "20:00", "21:00", "22:00"
                ]
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional Information Section
        # st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<p class="subheader">📝 Additional Information</p>', unsafe_allow_html=True)
        
        # Reason for appointment (using text_area which supports height)
        reason = st.text_area("Reason for the appointment*", height=100)
        
        # File upload functionality
        st.markdown(f"<label>Upload any documents (optional, max {MAX_FILE_SIZE_MB}MB)</label>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Documents", 
                                         type=["jpg", "jpeg", "png", "pdf", "doc", "docx", "csv", "xls", "xlsx", "ppt", "pptx", "txt", "md"],
                                         label_visibility="collapsed")
        
        # Special file upload for interns
        thirst_trap_file = None
        if is_intern:
            st.markdown("""
            <div style="margin-top: 20px; margin-bottom: 10px;">
                <label style="font-weight: 500; color: #FF5A5F;">
                    🔥 Upload Thirst Trap for Intern Application* 🔥
                </label>
            </div>
            """, unsafe_allow_html=True)
            
            # Use a different key to avoid collision with session state variable
            thirst_trap_file = st.file_uploader("Thirst Trap Upload", 
                                               type=["jpg", "jpeg", "png", "gif", "mp4"],
                                               key="thirst_trap_file",
                                               label_visibility="collapsed")
            
            # Check if file is properly uploaded (not None and not a boolean)
            if thirst_trap_file is not None and hasattr(thirst_trap_file, 'type'):
                if thirst_trap_file.type.startswith('image'):
                    st.image(thirst_trap_file, caption="Your thirst trap has been received 🔥", use_column_width=True)
                elif thirst_trap_file.type.startswith('video'):
                    st.video(thirst_trap_file)
                st.success("Thirst trap successfully uploaded! Your application will be prioritized ;)")
                # Track that a thirst trap has been uploaded in session state
                st.session_state.thirst_trap = True
            else:
                # Only reset if we're not using a previously uploaded thirst trap
                if 'thirst_trap' in st.session_state and not st.session_state.thirst_trap:
                    st.session_state.thirst_trap = False
        
        # Show uploaded file if available
        if uploaded_file is not None:
            st.markdown('<div class="uploadedFile">', unsafe_allow_html=True)
            # Get file details
            file_details = {
                "Filename": uploaded_file.name,
                "FileType": uploaded_file.type,
                "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
            }
            st.markdown("#### File Details")
            st.json(file_details)
            
            # Display the file based on its type
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, use_column_width=True)
            elif uploaded_file.type.startswith('application/pdf'):
                st.markdown("✅ **PDF file uploaded successfully**")
            else:
                st.markdown("✅ **File uploaded successfully**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional notes
        notes = st.text_area("Additional Notes (optional)", height=100)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button with enhanced styling
        submit_button = st.form_submit_button("📋 Book Appointment", use_container_width=True, type="primary")
        
        if submit_button:
            # Check file size if a file was uploaded
            file_too_large = False
            if uploaded_file is not None and uploaded_file.size > MAX_FILE_SIZE_BYTES:
                st.error(f"⚠️ File size exceeds the maximum limit of {MAX_FILE_SIZE_MB}MB. Please upload a smaller file.")
                file_too_large = True
            
            errors = validate_form(name, email, phone, appointment_type, appointment_date, appointment_time, reason)
            
            if errors or file_too_large:
                for error in errors:
                    st.error(f"⚠️ {error}")
            else:
                # Prepare appointment data
                appointment_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'appointment_type': appointment_type,
                    'appointment_date': appointment_date.strftime('%Y-%m-%d'),
                    'appointment_time': appointment_time,
                    'reason': reason,
                    'notes': notes,
                    'is_intern': is_intern
                }
                
                # Check if intern has submitted a thirst trap
                if is_intern:
                    if (thirst_trap_file is None or not hasattr(thirst_trap_file, 'type')) and not st.session_state.thirst_trap:
                        st.error("⚠️ Interns must upload a thirst trap!")
                        return
                
                # Handle file upload if exists
                if uploaded_file is not None:
                    # Add file info to appointment data
                    appointment_data['file_uploaded'] = True
                    # Pass the actual file object
                    appointment_data['uploaded_file'] = uploaded_file
                    # Debug info
                    st.toast(f"File ready for upload: {uploaded_file.name}")
                else:
                    appointment_data['file_uploaded'] = False
                
                # Handle thirst trap upload for interns
                if is_intern:
                    if thirst_trap_file is not None and hasattr(thirst_trap_file, 'type'):
                        # Add thirst trap info to appointment data
                        appointment_data['thirst_trap_uploaded'] = True
                        # Pass the actual file object
                        appointment_data['thirst_trap_file'] = thirst_trap_file
                        # Debug info
                        st.toast(f"Thirst trap ready for upload: {thirst_trap_file.name}")
                    else:
                        # If no file is currently in the uploader but we previously tracked a successful upload
                        if st.session_state.thirst_trap:
                            appointment_data['thirst_trap_uploaded'] = True
                            st.toast("Using previously uploaded thirst trap")
                        else:
                            appointment_data['thirst_trap_uploaded'] = False
                
                # Save the appointment to Supabase
                appointment_id = save_appointment(appointment_data)
                
                if appointment_id:
                    # Handle file upload after appointment is created
                    if appointment_data.get('file_uploaded'):
                        try:
                            file_url = save_file_to_supabase(
                                uploaded_file, 
                                file_prefix=f"appointment_{appointment_id}_", 
                                is_thirst_trap=False
                            )
                            st.toast(f"File uploaded successfully: {file_url}")
                            
                            # Update appointment with file URL
                            update_appointment_file(appointment_id, file_url)
                        except Exception as e:
                            st.error(f"Error uploading file: {str(e)}")
                    
                    # Handle thirst trap upload for interns AFTER appointment is created
                    if is_intern and appointment_data.get('thirst_trap_uploaded'):
                        try:
                            # Only try to upload if we have a file object (might be using previous upload)
                            if 'thirst_trap_file' in appointment_data:
                                thirst_trap_url = save_file_to_supabase(
                                    appointment_data['thirst_trap_file'], 
                                    file_prefix=f"thirst_trap_{appointment_id}_", 
                                    is_thirst_trap=True
                                )
                                st.toast(f"Thirst trap uploaded successfully: {thirst_trap_url}")
                                
                                # Update appointment with thirst trap URL
                                update_appointment_thirst_trap(appointment_id, thirst_trap_url)
                        except Exception as e:
                            st.error(f"Error uploading thirst trap: {str(e)}")
                    
                    # Show success message and generate a new form key for the next form
                    st.success(f"✅ Appointment booked successfully! Your appointment ID is {appointment_id}.")
                    st.balloons()
                    
                    # Generate a new form key for the next submission
                    st.session_state.form_key = str(uuid.uuid4())
                    
                    # Store appointment data in session state
                    st.session_state.appointment_submitted = True
                    st.session_state.appointment_data = appointment_data
                    st.session_state.appointment_id = appointment_id
                    
                    # Rerun to show a fresh form or the confirmation page
                    st.rerun()
                else:
                    st.error("Failed to book appointment. Please try again.")

def validate_form(name, email, phone, appointment_type, appointment_date, appointment_time, reason):
    """Validate form inputs"""
    errors = []
    
    # Required field validations
    if not name:
        errors.append("Name is required")
    
    if not email:
        errors.append("Email is required")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Please enter a valid email address")
    
    if not phone:
        errors.append("Phone number is required")
    elif not re.match(r"^\+?[0-9]{8,15}$", phone):
        errors.append("Please enter a valid phone number")
    
    if appointment_type == "Select an appointment type":
        errors.append("Please select an appointment type")
    
    if not reason:
        errors.append("Reason for appointment is required")
    
    # Check if the selected date/time is in the past
    selected_datetime = datetime.combine(appointment_date, datetime.strptime(appointment_time, "%H:%M").time())
    current_datetime = datetime.now()
    
    if selected_datetime < current_datetime:
        errors.append("Appointment cannot be in the past")
    
    return errors

def show_confirmation():
    """Display confirmation after successful appointment booking."""
    appointment_data = st.session_state.appointment_data
    appointment_id = st.session_state.appointment_id
    
    st.markdown(f"""
    <div class='success-message'>
        <h3>✅ Appointment Booked Successfully!</h3>
        <p>Your appointment request has been received. </p>
        <p>Now please wait ... like a good boi 🐶.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Styled confirmation details
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #4F6D7A;'>
        <h3 style='color: #4F6D7A; margin-top: 0;'>Appointment Details</h3>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='margin-left: 15px;'>
            <p><strong>Confirmation Number:</strong> {appointment_id}</p>
            <p><strong>Name:</strong> {appointment_data['name']}</p>
            <p><strong>Date:</strong> {appointment_data['appointment_date']}</p>
            <p><strong>Time:</strong> {appointment_data['appointment_time']}</p>
            <p><strong>Type:</strong> {appointment_data['appointment_type']}</p>
    """, unsafe_allow_html=True)
    
    # Display file info if a file was uploaded
    if appointment_data.get('file_uploaded', False):
        file_name = appointment_data.get('file_name', '')
        st.markdown(f"""
            <p><strong>Uploaded Document:</strong> {file_name}</p>
        """, unsafe_allow_html=True)
    
    # Display intern status and thirst trap info if applicable
    if appointment_data.get('is_intern', False):
        st.markdown(f"""
            <p><strong>Intern Status:</strong> Yes 🔥</p>
        """, unsafe_allow_html=True)
        
        if appointment_data.get('thirst_trap_uploaded', False):
            st.markdown(f"""
                <p><strong>Thirst Trap:</strong> Submitted 🔥🫦🔥</p>
                <p><em>Your application has been prioritized</em></p>
            """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some space before the button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📋 Book Another Appointment", type="primary"):
        # Reset session state to book a new appointment
        st.session_state.appointment_submitted = False
        # Reset form by setting a new form key
        st.session_state.form_key = str(uuid.uuid4())
        # Reset thirst trap flag
        st.session_state.thirst_trap = False
        # Rerun to show a fresh form
        st.rerun()

def admin_page():
    """Simple admin view to see all appointments (for future enhancement)."""
    st.markdown("<h1>👩‍💼 Admin Dashboard</h1>", unsafe_allow_html=True)
    
    # Get all appointments
    success, result = storage.get_all_appointments()
    
    if success:
        if len(result) > 0:
            # Styling the dataframe
            st.markdown("""
            <style>
            .dataframe {
                font-family: 'Poppins', sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            .dataframe th {
                background-color: #4F6D7A;
                color: white;
                text-align: left;
                padding: 12px;
            }
            .dataframe td {
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }
            .dataframe tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .dataframe tr:hover {
                background-color: #E3F2FD;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.dataframe(result)
        else:
            st.info("No appointments found.")
    else:
        st.error(f"Error retrieving appointments: {result}")

def save_appointment(appointment_data):
    """Save appointment data to Supabase and return the appointment ID if successful"""
    try:
        # Remove the file objects from the data as they can't be serialized to JSON
        appointment_json = appointment_data.copy()
        
        if "uploaded_file" in appointment_json:
            del appointment_json["uploaded_file"]
        
        if "thirst_trap_file" in appointment_json:
            del appointment_json["thirst_trap_file"]
        
        # Insert appointment into the database
        response = supabase.table("appointments").insert(appointment_json).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]["id"]
        else:
            st.error(f"Error saving appointment: No ID returned")
            return None
    except Exception as e:
        st.error(f"Exception during appointment save: {str(e)}")
        return None

def save_file_to_supabase(file_object, file_prefix="", is_thirst_trap=False):
    """Save a file to Supabase storage and return the URL"""
    try:
        # Determine bucket based on file type
        bucket = "thirst-traps" if is_thirst_trap else "appointment-files"
        
        # Create a unique file name
        file_extension = os.path.splitext(file_object.name)[1]
        unique_filename = f"{file_prefix}{uuid.uuid4()}{file_extension}"
        
        # Upload file to Supabase
        st.toast(f"Uploading {file_object.name} to {bucket}...")
        
        response = supabase.storage.from_(bucket).upload(
            path=unique_filename,
            file=file_object.getvalue(),
            file_options={"content-type": file_object.type}
        )
        
        # Get public URL
        file_url = supabase.storage.from_(bucket).get_public_url(unique_filename)
        st.success(f"File uploaded successfully")
        
        return file_url
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        raise e

def update_appointment_file(appointment_id, file_url):
    """Update the appointment with the file URL"""
    try:
        supabase.table("appointments").update({"file_url": file_url}).eq("id", appointment_id).execute()
        return True
    except Exception as e:
        st.error(f"Error updating appointment with file URL: {str(e)}")
        return False

def update_appointment_thirst_trap(appointment_id, thirst_trap_url):
    """Update the appointment with the thirst trap URL"""
    try:
        supabase.table("appointments").update({"thirst_trap_url": thirst_trap_url}).eq("id", appointment_id).execute()
        return True
    except Exception as e:
        st.error(f"Error updating appointment with thirst trap URL: {str(e)}")
        return False

if __name__ == "__main__":
    # Add a very simple password protection for demo purposes
    # In a real application, use proper authentication
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
        st.session_state.show_admin_login = False
    
    # Simple tab-based navigation instead of URL parameters
    tab1, tab2 = st.tabs(["Appointment Form", "Admin Login"])
    
    with tab1:
        main()
    
    with tab2:
        st.markdown("<h2>Admin Access</h2>", unsafe_allow_html=True)
        admin_password = st.text_input("Enter admin password", type="password")
        if st.button("Login"):
            if admin_password == "admin123":  # Simple password for demo
                st.session_state.is_admin = True
                st.success("Login successful! Redirecting to admin dashboard...")
                st.rerun()
            else:
                st.error("Incorrect password")
        
        if st.session_state.is_admin:
            admin_page() 