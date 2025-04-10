import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"Initializing Supabase client with URL: {SUPABASE_URL}")
print(f"Using key starting with: {SUPABASE_KEY[:5]}..." if SUPABASE_KEY else "WARNING: SUPABASE_KEY is not set!")

# Create Supabase client
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully")
except Exception as e:
    print(f"Error creating Supabase client: {e}")
    import traceback
    traceback.print_exc()
    raise

def initialize_database():
    """
    Initialize Supabase tables if needed.
    This is a no-op for Supabase since tables should be created in the dashboard.
    """
    return True

def save_file_to_supabase(file_content, file_name, bucket="uploads"):
    """
    Upload a file to Supabase Storage.
    
    Args:
        file_content: The binary content of the file
        file_name: Name of the file
        bucket: Supabase storage bucket name
        
    Returns:
        str: The path to the file in Supabase Storage
    """
    print(f"Starting upload of {file_name} to bucket {bucket}")
    
    try:
        # Check if the bucket exists
        buckets = supabase.storage.list_buckets()
        bucket_exists = any(b['name'] == bucket for b in buckets)
        
        if not bucket_exists:
            print(f"Bucket {bucket} doesn't exist. Available buckets: {[b['name'] for b in buckets]}")
            print(f"Creating bucket {bucket}...")
            supabase.storage.create_bucket(bucket)
            print(f"Bucket {bucket} created successfully")
    
        # Create a unique filename to prevent collisions
        unique_filename = f"{uuid.uuid4()}-{file_name}"
        print(f"Generated unique filename: {unique_filename}")
        
        # Upload the file
        print(f"Uploading {len(file_content)} bytes to {bucket}/{unique_filename}")
        upload_result = supabase.storage.from_(bucket).upload(unique_filename, file_content)
        print(f"Upload result: {upload_result}")
        
        # Get public URL
        file_path = supabase.storage.from_(bucket).get_public_url(unique_filename)
        print(f"Public URL: {file_path}")
        
        return file_path
    except Exception as e:
        print(f"Error uploading file to Supabase: {e}")
        import traceback
        traceback.print_exc()
        raise

def get_appointments_table():
    """
    Get a reference to the appointments table.
    """
    return supabase.table("appointments")

def appointment_to_dict(appointment):
    """
    Convert appointment data from Supabase to a dictionary.
    """
    # The data is already in dictionary format from Supabase
    return appointment

def test_connection():
    """Test the Supabase connection and return True if successful."""
    try:
        # Try to fetch a single row from appointments table
        supabase.table("appointments").select("*").limit(1).execute()
        return True, "Supabase connection successful!"
    except Exception as e:
        return False, f"Supabase connection failed: {str(e)}" 