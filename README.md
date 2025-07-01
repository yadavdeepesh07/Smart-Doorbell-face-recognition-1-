# 🔔 Smart Doorbell with Face Recognition

A Python-powered smart doorbell system that captures live video, detects and recognizes known faces using AWS Rekognition, and sends real-time alerts via email and SMS. Includes a web dashboard to manage known visitors and log every entry with a snapshot.

---

## ✨ Features

- 🎥 Real-time video feed via OpenCV
- 🧠 Face recognition with AWS Rekognition
- 📬 Email alerts via Gmail
- 📲 SMS alerts via Twilio
- 🖼️ Visitor snapshot logging
- 🌐 Web dashboard to manage users
- 🔒 Environment-based secret handling

---

## 🧰 Tech Stack

- Python 3.8+
- OpenCV
- Flask
- AWS Rekognition
- Twilio SMS
- Gmail SMTP
- dotenv

---

## 🗂️ Project Structure

Smart_Doorbell_with_Face_Recognition/
│
├── run.py                          # 🔁 Main script to start the camera + detection

├── dashboard.py                    # 📊 Flask web dashboard (UI)

├── requirements.txt                # 📦 Python dependencies

├── .env                            # 🔐 Environment variables (email creds, AWS, etc.)

├── test/

    ├── test_aws.py
    
    ├── test_rekognition.py
    
├── start_smart_doorbell.bat

├── venv                       # Environment for the project 
│
├── app/                            # 📁 Core backend logic

│   ├── __init__.py
│   ├── aws_rekognition.py          # 🔍 AWS face search, index, delete, etc.

│   ├── config.py                   # ⚙️  Read/write environment or JSON config

│   ├── visitor_log.py              # 📝 JSON + CSV logging for known/unknown visitors

│   ├── notification.py             # ✉️  Email (and SMS if enabled) alerts

│   └── sms_alert.py                # 📱 (Optional) Twilio SMS alerts (if enabled)

│
├── logs/                           # 🗃️ Visitor log files

│   ├── visitor_log.json            # ✅ Visitor log in JSON

│   ├── visitor_log.csv             # ✅ Visitor log in CSV

│   └── snapshots/                  # 🖼️  Original captured frames
│       └── [name_timestamp].jpg

│
├── static/                         # 🌐 Static files served to frontend

│   ├── snapshots/                  # 🖼️ Snapshots used by dashboard

│   └── uploads/                    # 📤 Uploaded images for adding users
│
├── templates/                      # 📄 HTML pages (Flask Jinja2 templates)

│   ├── index.html                  # 🏠 Home (optional or redirect)

│   ├── visitors.html               # 📋 Visitor log UI

│   ├── manage_user.html

    ├── privacy.html



---

## 🔧 Setup Instructions

1. **Clone the repo**

git clone https://github.com/yadavdeepesh07/smart-doorbell-face-recognition.git

cd smart-doorbell-face-recognition

2. Create a virtual environment

python -m venv venv

venv\Scripts\activate      # Windows

source venv/bin/activate   # macOS/Linux

4. Install dependencies

we have added in requirements.txt 

pip install -r requirements.txt

if facing issue then install maunally one by one 

6. Create a .env file with your AWS Rekognition and Gmail SMTP credentials

follow the following Structure
   
# AWS

AWS_ACCESS_KEY_ID=your_key

AWS_SECRET_ACCESS_KEY=your_secret

AWS_REGION=us-east-1

# Email

EMAIL_ADDRESS=your_email@gmail.com

EMAIL_PASSWORD=your_app_password

# Twilio

TWILIO_ACCOUNT_SID=your_sid

TWILIO_AUTH_TOKEN=your_token

TWILIO_PHONE=+1234567890

USER_PHONE=+919xxxxxxxxx

5. Run the 
    1. Live Face Detection & Alerts
   
    python run.py
   
    2. Launch Web Dashboard
   
    python dashboard.py

Screenshots

![Screenshot 2025-07-01 165750](https://github.com/user-attachments/assets/b506d916-b1f2-4c26-b575-e1998673b168)

![Screenshot 2025-07-01 165813](https://github.com/user-attachments/assets/9460ebca-90f9-43f0-b313-5539eb49ed8e)

![Screenshot 2025-07-01 165739](https://github.com/user-attachments/assets/4cef5d99-7fb2-4ccf-a882-0e4ae2f7b9e2)




Security Notes

✅ Never commit .env or real credentials

✅ AWS keys are required only for face recognition, not for UI

✅ GitHub blocks pushes with leaked secrets

🧠 Credits

AWS Rekognition

Twilio

OpenCV

Flask
