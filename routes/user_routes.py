from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import db
import re

# Create a blueprint for user-related routes
user_bp = Blueprint('user', __name__)

# Helper function to validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Helper function to check password strength
def is_strong_password(password):
    return len(password) >= 6

# Route for user registration
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Validate input fields
    if not username or not email or not password or not role:
        return jsonify({"error": "All fields are required"}), 400

    # Validate role
    if role not in ['consumer', 'chef']:
        return jsonify({"error": "Invalid role"}), 400

    # Validate email format
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Validate password strength
    if not is_strong_password(password):
        return jsonify({"error": "Password is too weak"}), 400

    # Check if user with the same email or username already exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"error": "User with this email or username already exists"}), 400

    # Hash the password and create a new user
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, email=email, password=hashed_password, role=role)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Route for user login
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find the user by email
    user = User.query.filter_by(email=email).first()
    
    # Check if the user exists and the password is correct
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Logged in successfully"}), 200

