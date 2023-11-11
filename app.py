from flask import Flask
from main import main_blueprint, create_app
from admin import admin_blueprint
import secrets

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
secret_key = secrets.token_hex(24)  # You can adjust the key length as needed

# Set the secret key for your Flask application
app.secret_key = secret_key
# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/rentacar'

# Register the main blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
# Initialize the db instance with your Flask app
create_app(app)

if __name__ == "__main__":
    app.run(debug=True)
