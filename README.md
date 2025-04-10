# 📅 Xiaoyue's Appointment Form

A stylish, modern appointment booking application built with Python, Streamlit, and Supabase.

![Appointment Form Screenshot](data/screenshots/appointment_form.png)

## ✨ Features

- **User-friendly appointment booking form**
- **Modern, stylish UI with Poppins font**
- **Mobile-responsive design**
- **Form validation with error messages**
- **File upload capability (max 20MB)**
- **Supabase integration for data storage**
- **Special intern application feature with thirst trap upload**
- **Confirmation page after successful booking**
- **Basic admin dashboard**

## 📋 Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd appointment_form
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Supabase Setup

This application uses Supabase for data storage and file uploads. Follow these steps to set up your Supabase project:

1. Create a free account at [Supabase](https://supabase.com/)
2. Create a new project
3. Create the following tables:
   - `appointments` - for storing appointment data
4. Set up storage buckets:
   - Create a bucket called `appointment-files` for regular file uploads
   - Create a bucket called `thirst-traps` for intern application photos/videos
5. Set your storage buckets to public access (or configure appropriate RLS policies)

## 🔑 Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

## 🚀 Running Locally

To run the application on your local machine:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## 👩‍💼 Accessing Admin Dashboard

The application includes a basic admin dashboard to view submitted appointments:

1. Navigate to the "Admin Login" tab
2. Enter the password: `admin123` (change this in production)

## 📱 Using the Application

### Standard Appointment Booking
1. Fill out the required personal information
2. Select appointment type, date, and time
3. Provide reason for the appointment
4. Optionally upload relevant documents
5. Click "Book Appointment"

### Intern Applications
The application includes a special feature for intern applicants:
1. Check the "Are you an intern?" box
2. Complete the standard appointment form
3. Upload a "thirst trap" image or video (required for intern applications)
4. Your application will be prioritized 🔥

## 🌐 Deployment Options

### 1. Streamlit Cloud (Recommended)

The easiest way to make your app available to others:

1. Push your code to a GitHub repository
2. Sign up at [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account and select your repository
4. Set the required environment variables in the Streamlit Cloud settings
5. Your app will be deployed with a public URL

### 2. Self-hosting on VPS

For a permanent solution on your own server:

1. Set up a VM on AWS, GCP, or DigitalOcean
2. Clone the repo and install dependencies
3. Set up your environment variables
4. Run with:
```bash
streamlit run app.py --server.headless=true --server.enableCORS=false
```
5. Configure your domain and SSL certificates

## 🎨 Customization

### Appointment Types

Modify the `APPOINTMENT_TYPES` list in `app.py`:

```python
APPOINTMENT_TYPES = [
    "Career Development",
    "Routine Check-up",
    "Urgent Care",
    "Performance Evaluation"
]
```

### Time Slots

Change the available times in the selectbox options:

```python
appointment_time = st.selectbox(
    "Preferred Time*",
    options=[
        "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"
        # Add or remove times as needed
    ]
)
```

### Styling

The app uses a custom CSS styling with the Poppins font and a color scheme defined in the CSS variables. You can modify these in the `st.markdown()` section at the beginning of `app.py`.

## 🔄 Future Enhancements

- Email notifications for appointments
- Calendar integration
- Enhanced admin dashboard with more features
- User authentication system
- Time slot availability checking
- Enhanced security for file uploads

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please contact xiaoyuezhuu@gmail.com
