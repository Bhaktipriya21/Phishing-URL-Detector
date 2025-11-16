from flask import Flask, render_template, request, session, redirect, url_for, flash
import pickle
import os
import random # For dummy prediction

# --- 1. Model Setup ---

model = None
try:
    # Assuming 'pickle/model.pkl' is the trained model file (e.g., Random Forest or another classifier)
    # NOTE: The real model file is not available, so we include a dummy prediction function below
    model = pickle.load(open('pickle/model.pkl', 'rb'))
    print("Phishing Detection Model loaded successfully.")
except FileNotFoundError:
    print("WARNING: Model file 'pickle/model.pkl' not found. Using dummy prediction.")
except Exception as e:
    print(f"Error loading model: {e}. Using dummy prediction.")


# --- 2. Dummy Feature/Prediction Function (Simulating external feature.py) ---

def get_prediction_from_url(url, model):
    """
    Simulates the function from feature.py:
    Takes a URL and returns a prediction result (1 for Safe/Legitimate, 0 for Phishing/Suspicious)
    """
    # Simple dummy logic for demonstration when the real model is not loaded
    if model is None:
        # Dummy behavior: If URL contains common phishing keywords, return 0 (Suspicious)
        if any(keyword in url.lower() for keyword in ["login", "verify", "security", "update", "bank"]):
            return 0
        return 1 # Default to safe if model isn't loaded

    # If the model is loaded, assume we have the feature extraction logic 
    # For a placeholder, we use a random prediction for a live-feeling app
    if random.random() < 0.2: # 20% chance of being suspicious
         return 0
    return 1 


# --- 3. Flask App Setup ---

app = Flask(__name__)
# IMPORTANT: Set a secret key for session management (mandatory for login functionality)
app.secret_key = 'super_secret_url_phishing_key_456' 

# --- 4. Routing and Navigation ---

# Home Page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', page='home', logged_in='user' in session)

# About Us Page
@app.route('/about', methods=['GET'])
def about():
    return render_template('index.html', page='about', logged_in='user' in session)

# Contact Page
@app.route('/contact', methods=['GET'])
def contact():
    return render_template('index.html', page='contact', logged_in='user' in session)

# New Placeholder Page
@app.route('/design', methods=['GET'])
def design():
    return render_template('index.html', page='design', logged_in='user' in session)


# Login Route (Simulated)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simple check: If an email/username is provided, login is successful.
        email = request.form.get('email') or request.form.get('username') 
             
        if email: 
            session['user'] = email
            flash(f'Login successful for {email}!', 'success')
            return redirect(url_for('service'))
        else:
            flash('Please enter your email/username to log in.', 'danger')
            return render_template('index.html', page='login', logged_in=False)
            
    return render_template('index.html', page='login', logged_in='user' in session)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Service/Detector Page (Protected) - Handles both GET and POST for prediction
@app.route('/service', methods=['GET', 'POST'])
def service():
    if 'user' not in session:
        flash('Please log in to access the URL Detector Service.', 'warning')
        return redirect(url_for('login'))
        
    prediction_result = None
    submitted_url = ""
    
    if request.method == 'POST':
        # Input field name from the template: url_to_check
        submitted_url = request.form.get('url_to_check')
        
        if not submitted_url:
            prediction_result = "Please enter the URL to check."
        else:
            # Use the simulated prediction function from the external feature module
            prediction = get_prediction_from_url(submitted_url, model)

            if prediction == 1:
                # 1 = Legitimate/Safe URL
                prediction_result = 'Safe URL (सुरक्षित URL)'
            else:
                # 0 = Phishing/Suspicious URL
                prediction_result = 'Suspicious URL (संभाव्य धोकादायक)'

        
    return render_template('index.html', 
                           page='service',
                           logged_in='user' in session,
                           prediction_result=prediction_result, 
                           mail_content=submitted_url)

if __name__ == "__main__":
    app.run(debug=True)