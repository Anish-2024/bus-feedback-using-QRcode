from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env (for local dev)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "defaultsecret")  # Optional default fallback

# ✅ Use MONGO_URI from environment variable (IMPORTANT!)
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client["bus_feedback"]
feedbacks_collection = db["feedbacks"]

# Home route
@app.route('/')
def home():
    return "<h2>✅ Server is Running! Use /feedback?bus=KA25B1221 to submit feedback or /admin to view feedbacks.</h2>"

# Feedback form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    bus_id = request.args.get('bus')
    if request.method == 'POST':
        data = {
            "bus_id": bus_id,
            "category": request.form['category'],
            "message": request.form['message'],
            "timestamp": datetime.now()
        }
        feedbacks_collection.insert_one(data)
        return render_template("success.html")
    return render_template("feedback_form.html", bus_id=bus_id)

# Admin login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "❌ Invalid credentials!"
    return render_template("login.html")

# Admin logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

# Admin dashboard
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    feedbacks = list(feedbacks_collection.find().sort("timestamp", -1))
    return render_template("admin.html", feedbacks=feedbacks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
