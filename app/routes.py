# from flask import Blueprint , render_template

# main = Blueprint('main', __name__)

# @main.route('/')
# def index():
#     return render_template('index.html')
from flask import Blueprint, render_template, send_from_directory
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join('templates', 'js'), filename)


# Catch-all route for 404 errors
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
