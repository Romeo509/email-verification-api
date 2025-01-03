from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
import random
import string
import os
from dotenv import load_dotenv 

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__, static_url_path='')

# Flask-Mail configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

# In-memory user data store
users = {}
verification_codes = {}

# Function to generate a random verification code
def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Serve the static HTML signup page
@app.route('/')
def serve_signup_page():
    return send_from_directory('', 'index.html')

# Endpoint: POST /signup
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["username", "email", "password", "confirmPassword"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required"}), 400

        username = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirmPassword"]

        # Check if passwords match
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        # Ensure password is at least 8 characters
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        # Check if email already exists
        if email in users:
            return jsonify({"error": "Email already exists"}), 400

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Generate and store the verification code
        verification_code = generate_verification_code()
        verification_codes[email] = verification_code

        try:
            # Send verification email
            msg = Message("Verify Your Email", sender=app.config["MAIL_USERNAME"], recipients=[email])
            msg.body = f"Your verification code is: {verification_code}"
            mail.send(msg)
        except Exception as e:
            return jsonify({"error": "Failed to send verification email", "details": str(e)}), 500

        # Save user data without activation
        users[email] = {"username": username, "password": hashed_password, "verified": False}
        return jsonify({"message": "User registered successfully. Please verify your email."}), 201
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500

# Endpoint: POST /verify-email
@app.route('/verify-email', methods=['POST'])
def verify_email():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["email", "verificationCode"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required"}), 400

        email = data["email"]
        verification_code = data["verificationCode"]

        # Check if user exists
        if email not in users:
            return jsonify({"error": "User does not exist"}), 400

        # Check if verification code matches
        if email not in verification_codes or verification_codes[email] != verification_code:
            return jsonify({"error": "Invalid or expired verification code"}), 400

        # Mark user as verified and remove the verification code
        users[email]["verified"] = True
        del verification_codes[email]
        return jsonify({"message": "Verification successful."}), 200
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
