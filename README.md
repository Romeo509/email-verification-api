# Flask Email Verification System

## Overview
This project is a Flask-based application that enables user signup with email verification. The app ensures secure user registration by validating user credentials, hashing passwords, and requiring email verification before completing the signup process.

## Features
- **User Registration**: Accepts username, email, and password during signup.
- **Password Validation**: Ensures passwords are at least 8 characters long and match the confirmation password.
- **Email Verification**: Sends a 6-digit verification code to the user's email address.
- **Verification Code Validation**: Verifies the user using the code sent to their email.
- **Secure Passwords**: Hashes passwords for storage.

## Technologies Used
- **Flask**: Backend framework for handling API routes and server-side logic.
- **Flask-Mail**: Library for sending email verification codes.
- **Werkzeug Security**: Utility for hashing passwords.
- **dotenv**: For managing environment variables.

## Setup Instructions

### Prerequisites
1. Python 3.8 or higher installed.
2. A Gmail account to send verification emails.
3. Required Python packages installed (see `requirements.txt`).

### Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

   
### Install dependencies:
```bash
pip install -r requirements.txt
```

### Set up environment variables: 
Create a .env file in the root directory and add the following:
```bash
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
PORT=5000

```

### Run the application
```bash
python app.py
```

