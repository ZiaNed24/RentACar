from flask import Flask
from main import main_blueprint, create_app
from admin import admin_blueprint
from decouple import config  # Import config from python-decouple

app = Flask(__name__)

# Read the secret key from the .env file
secret_key = config('SECRET_KEY')

# Set the secret key for your Flask application
app.secret_key = secret_key

# Read the database URI from the .env file
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')

# Register the main blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')

# Initialize the db instance with your Flask app
create_app(app)

if __name__ == "__main__":
    app.run(debug=True)
