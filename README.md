# 📅 Xiaoyue's Appointment Form

A stylish, mobile-friendly web application for booking appointments, built with Python and Streamlit.

![Appointment Form Screenshot](data/screenshots/appointment_form.png)

## ✨ Features

- **User-friendly appointment booking form**
- **Modern, stylish UI with Poppins font**
- **Mobile-responsive design**
- **Form validation with error messages**
- **File upload capability (max 20MB)**
- **Confirmation page after successful booking**
- **Data storage in CSV format**
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

## 🚀 Running Locally

To run the application on your local machine:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## 👩‍💼 Accessing Admin Dashboard

The application includes a basic admin dashboard to view submitted appointments:

1. Add `?view=admin` to the URL: http://localhost:8501/?view=admin
2. Enter the password: `admin123` (change this in production)

## 🌐 Deployment Options for Remote Access

### 1. Streamlit Cloud (Recommended)

The easiest way to make your app available to others:

1. Push your code to a GitHub repository
2. Sign up at [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account and select your repository
4. Your app will be deployed with a public URL like `https://yourusername-appointment-form.streamlit.app`

### 2. Heroku

To deploy on Heroku:

1. Create a `Procfile` in the root directory:
```
web: streamlit run --server.port $PORT app.py
```

2. Add a `runtime.txt` file:
```
python-3.11.0
```

3. Deploy using Heroku CLI:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### 3. Temporary Sharing with Ngrok

For quick temporary sharing:

1. Install ngrok: `pip install pyngrok`
2. Run your app: `streamlit run app.py`
3. In a new terminal: `ngrok http 8501`
4. Share the ngrok URL (valid for a few hours)

### 4. Self-hosting on VPS

For a permanent solution on your own server:

1. Set up a VM on AWS, GCP, or DigitalOcean
2. Clone the repo and install dependencies
3. Run with:
```bash
streamlit run app.py --server.headless=true --server.enableCORS=false
```
4. Configure your domain and SSL certificates

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
- Database storage (SQL/NoSQL) instead of CSV
- Enhanced admin dashboard with more features
- User authentication system
- Time slot availability checking

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please contact xiaoyuezhuu@gmail.com
