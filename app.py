import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from utils import validation, storage

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
    
    .stButton button:hover {
        background-color: var(--primary-color) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
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
    # Initialize storage
    storage.initialize_storage()
    
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
            min_date = datetime.now().date() + timedelta(days=1)
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
        if is_intern:
            st.markdown("""
            <div style="margin-top: 20px; margin-bottom: 10px;">
                <label style="font-weight: 500; color: #FF5A5F;">
                    🔥 Upload Thirst Trap for Intern Application* 🔥
                </label>
            </div>
            """, unsafe_allow_html=True)
            
            thirst_trap_file = st.file_uploader("Thirst Trap Upload", 
                                               type=["jpg", "jpeg", "png", "gif", "mp4"],
                                               key="thirst_trap",
                                               label_visibility="collapsed")
            
            if thirst_trap_file is not None:
                if thirst_trap_file.type.startswith('image'):
                    st.image(thirst_trap_file, caption="Your thirst trap has been received 🔥", use_column_width=True)
                elif thirst_trap_file.type.startswith('video'):
                    st.video(thirst_trap_file)
                st.success("Thirst trap successfully uploaded! Your application will be prioritized.")
        
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
        submit_button = st.form_submit_button("📋 Book Appointment")
        
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
                
                # Handle file upload if exists
                if uploaded_file is not None:
                    # Create uploads directory if it doesn't exist
                    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'uploads')
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir)
                    
                    # Save the file
                    file_path = os.path.join(upload_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Add file info to appointment data
                    appointment_data['file_uploaded'] = True
                    appointment_data['file_name'] = uploaded_file.name
                    appointment_data['file_path'] = file_path
                else:
                    appointment_data['file_uploaded'] = False
                
                # Handle thirst trap upload for interns
                if is_intern:
                    if thirst_trap_file is not None:
                        # Create thirst trap upload directory if it doesn't exist
                        thirst_trap_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'thirst_traps')
                        if not os.path.exists(thirst_trap_dir):
                            os.makedirs(thirst_trap_dir)
                        
                        # Save the thirst trap file
                        thirst_trap_path = os.path.join(thirst_trap_dir, thirst_trap_file.name)
                        with open(thirst_trap_path, "wb") as f:
                            f.write(thirst_trap_file.getbuffer())
                        
                        # Add thirst trap info to appointment data
                        appointment_data['thirst_trap_uploaded'] = True
                        appointment_data['thirst_trap_filename'] = thirst_trap_file.name
                        appointment_data['thirst_trap_path'] = thirst_trap_path
                    else:
                        appointment_data['thirst_trap_uploaded'] = False
                
                # Save appointment
                success, result = storage.save_appointment(appointment_data)
                
                if success:
                    # Update session state
                    st.session_state.appointment_submitted = True
                    st.session_state.appointment_id = result
                    st.session_state.appointment_data = appointment_data
                    st.session_state.form_key += 1  # Increment form key to prevent resubmission
                    
                    # Rerun to show confirmation
                    st.rerun()
                else:
                    st.error(f"Error saving appointment: {result}")

def validate_form(name, email, phone, appointment_type, appointment_date, appointment_time, reason):
    """Validate all form fields and return a list of error messages."""
    errors = []
    
    # Validate name
    valid, message = validation.validate_name(name)
    if not valid:
        errors.append(message)
    
    # Validate email
    valid, message = validation.validate_email(email)
    if not valid:
        errors.append(message)
    
    # Validate phone
    valid, message = validation.validate_phone(phone)
    if not valid:
        errors.append(message)
    
    # Validate appointment type
    valid, message = validation.validate_appointment_type(appointment_type, APPOINTMENT_TYPES)
    if not valid:
        errors.append(message)
    
    # Validate appointment date and time
    valid, message = validation.validate_appointment_date(
        appointment_date.strftime('%Y-%m-%d'), 
        appointment_time
    )
    if not valid:
        errors.append(message)
    
    # Validate reason
    if not reason or not reason.strip():
        errors.append("Please provide a reason for the appointment.")
    
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
        st.markdown(f"""
            <p><strong>Uploaded Document:</strong> {appointment_data['file_name']}</p>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # st.markdown("""
    # <div style='margin-top: 20px; padding: 15px; background-color: #E3F2FD; border-radius: 8px;'>
    #     <p style='margin: 0;'>You will receive a confirmation email shortly. Please check your inbox.</p>
    # </div>
    # """, unsafe_allow_html=True)
    
    # Add some space before the button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📋 Book Another Appointment"):
        # Reset session state to book a new appointment
        st.session_state.appointment_submitted = False
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

if __name__ == "__main__":
    # Add a very simple password protection for demo purposes
    # In a real application, use proper authentication
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
        
    # Simple URL parameter-based access to admin page (not secure)
    query_params = st.experimental_get_query_params()
    if 'view' in query_params and query_params['view'][0] == 'admin':
        admin_password = st.text_input("Enter admin password", type="password")
        if admin_password == "admin123":  # Simple password for demo
            st.session_state.is_admin = True
            admin_page()
        elif admin_password:
            st.error("Incorrect password")
        else:
            st.info("Enter password to access admin dashboard")
    else:
        main() 