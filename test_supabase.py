#!/usr/bin/env python3
"""
Supabase Connection Test Script

This script tests both the PostgreSQL database connection and Supabase Storage access.
It will help verify that your environment variables are set up correctly.
"""

import os
from dotenv import load_dotenv
from utils.db_connection import test_connection, supabase
import tempfile

# Load environment variables
load_dotenv()

def test_database():
    """Test the PostgreSQL database connection."""
    print("Testing PostgreSQL database connection...")
    success, message = test_connection()
    
    if success:
        print(f"✅ Database connection successful!")
    else:
        print(f"❌ Database connection failed: {message}")
    
    return success

def test_supabase_storage():
    """Test the Supabase Storage connection."""
    print("\nTesting Supabase Storage connection...")
    
    try:
        # Check if buckets exist
        buckets = supabase.storage.list_buckets()
        print(f"Found {len(buckets)} buckets:")
        for bucket in buckets:
            print(f"  - {bucket['name']}")
        
        # Create test buckets if they don't exist
        required_buckets = [
            os.getenv("UPLOAD_BUCKET", "uploads"),
            os.getenv("THIRST_TRAP_BUCKET", "thirst_traps")
        ]
        
        for bucket_name in required_buckets:
            bucket_exists = any(bucket['name'] == bucket_name for bucket in buckets)
            if not bucket_exists:
                print(f"Creating bucket '{bucket_name}'...")
                supabase.storage.create_bucket(bucket_name)
                print(f"✅ Created bucket '{bucket_name}'")
            else:
                print(f"✅ Bucket '{bucket_name}' already exists")
        
        # Test file upload to the uploads bucket
        print("\nTesting file upload to uploads bucket...")
        test_bucket = os.getenv("UPLOAD_BUCKET", "uploads")
        
        # Create a small temporary file
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp:
            temp.write(b"Hello, Supabase Storage!")
            temp.flush()
            
            # Upload the file
            test_file_path = f"test-{os.urandom(4).hex()}.txt"
            with open(temp.name, "rb") as f:
                supabase.storage.from_(test_bucket).upload(test_file_path, f)
            
            print(f"✅ Successfully uploaded test file '{test_file_path}'")
            
            # Delete the test file (cleanup)
            supabase.storage.from_(test_bucket).remove([test_file_path])
            print(f"✅ Successfully deleted test file '{test_file_path}'")
        
        print("\n✅ Supabase Storage connection successful!")
        return True
    
    except Exception as e:
        print(f"\n❌ Supabase Storage connection failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=== Supabase Connection Tests ===\n")
    
    db_success = test_database()
    storage_success = test_supabase_storage()
    
    print("\n=== Test Summary ===")
    print(f"Database Connection: {'✅ PASS' if db_success else '❌ FAIL'}")
    print(f"Storage Connection:  {'✅ PASS' if storage_success else '❌ FAIL'}")
    
    if db_success and storage_success:
        print("\n🎉 All tests passed! Your Supabase integration is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check your environment variables and Supabase settings.")

if __name__ == "__main__":
    main() 