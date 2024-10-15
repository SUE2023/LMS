#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask import Flask, redirect, url_for, request, flash
from flask_cors import CORS
from flasgger import Swagger
import bcrypt
from flask_login import LoginManager, UserMixin, login_user 
from flask_login import login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# SQLAlchemy configuration for MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning from SQLAlchemy
db = SQLAlchemy(app)  # Create an instance of SQLAlchemy

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: A resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)
    
# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirects to 'login' route if not logged in

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/index')
def index():
    return app.send_static_file('index.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


app.config['SWAGGER'] = {
    'title': 'Library Management System API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('LMS_API_HOST', '0.0.0.0')
    port = environ.get('LMS_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
