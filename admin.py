from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
from werkzeug.utils import secure_filename
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, render_template
from main import db,Contact,Reservation,Car
admin_blueprint = Blueprint('admin', __name__)
app = Flask(__name__)
# Generate a secret key for your app
secret_key = secrets.token_hex(24)
app.secret_key = secret_key

# Define the path for the 'uploads' folder
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

# Ensure the 'uploads' folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@admin_blueprint.route('/show_alert/<messages>')
def show_alert(messages):
    return render_template('admin/alert1.html', messages=messages)

@admin_blueprint.route('/show_alert4/<messages>')
def show_alert4(messages):
    return render_template('admin/alert4.html', messages=messages)





class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    images = db.Column(db.String(255))
    detail = db.Column(db.String(255))

@admin_blueprint.route('/adminindex')
def home():
    if 'user_id' in session:
        return render_template('/admin/adminindex.html')
    else:
        return redirect('/admin/')


@admin_blueprint.route('/add', methods=['GET'])
def add():
    if 'user_id' in session:
        return render_template('/admin/addproduct.html')
    else:
        return redirect('/admin/')

@admin_blueprint.route('/upload', methods=['POST'])
def add_car():
    if request.method == 'POST':
        # Get the list of uploaded files
        images = request.files.getlist("images")
        image_filenames = []

        for image in images:
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filenames.append(filename)

        # Convert the list of image filenames to a comma-separated string
        image_filenames_str = ','.join(image_filenames)
        name = request.form.get('name')
        desc = request.form.get('description')
        rent = request.form.get('rent')
        trans = request.form.get('trans')
        fuel = request.form.get('fuel')
        color = request.form.get('color')
        type = request.form.get('type')
        engine = request.form.get('engine')
        ac = request.form.get('ac')
        capacity = request.form.get('capacity')
        b_name = request.form.get('b_name')

        new_color = Car(b_name=b_name,name=name, images=image_filenames_str, description=desc, rent=rent, transmission=trans, type=type, engine=engine, ac=ac, color=color, fuel=fuel, capacity=capacity)
        db.session.add(new_color)
        db.session.commit()

        return redirect(url_for('admin.show_alert', messages='Car Is Placed'))

    return render_template('/admin/addproduct.html')

# Add your other routes here...







@admin_blueprint.route('/singless/<string:brand_name>', methods=['GET'])
def adminbranddetail(brand_name):
    # Fetch cars of the specified brand
    cars = db.session.query(Car).filter(Car.b_name == brand_name).all()

    # Fetch brand details
    brand = db.session.query(Brand).filter(Brand.name == brand_name).first()

    return render_template('admin/adminbranddetail.html', cars=cars, brand=brand)

@admin_blueprint.route("/adminbrands")
def adminbrands():
    new = Brand.query.all()
    return render_template("admin/adminbrands.html", new=new)

@admin_blueprint.route('/admincars')
def admincars():
    if 'user_id' in session:
        tasks = Car.query.all()
        return render_template('admin/admincars.html', tasks=tasks)
    else:
        return redirect('/admin/')


@admin_blueprint.route('/delete/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    task = Car.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/admin/admincars')

users = {}

# Email configuration
EMAIL_ADDRESS = 'zianawaz43210@gmail.com'  # Replace with your Gmail email
APP_PASSWORD = 'vuph iccj kltm lsrh'  # Replace with the App Password

def send_otp_email(recipient, otp):
    # Create an SMTP connection using the App Password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, APP_PASSWORD)

    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = "CAR RENT"
    msg['To'] = recipient
    msg['Subject'] = 'Your OTP for Login'
    msg.attach(MIMEText(f'Your OTP is: {otp}', 'plain'))

    # Send the email
    server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
    server.quit()

@admin_blueprint.route('/', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if 'generate_otp' in request.form:
            # Generate a random 6-digit OTP
            otp = ''.join(random.choices(string.digits, k=6))
            session['otp'] = otp
            c_email="zianeduet123@gmail.com"
            # Send the OTP via email
            send_otp_email(c_email, otp)

            return render_template('admin/adminlogin.html', message='OTP sent to your email.')

        elif 'login' in request.form:
            name = request.form.get('name')
            input_otp = request.form.get('input_otp', '')
            if input_otp == session.get('otp'):
                session['user_id'] = input_otp
                session['name'] = name
                ndata = Contact.query.order_by(Contact.id.desc()).all()
                return render_template('admin/adminindex.html',ndata=ndata)
            else:
                return render_template('admin/adminlogin.html')

    return render_template("admin/adminlogin.html")

@admin_blueprint.route('/logout')
def logout():
    # Clear the user ID from the session on logout
    session.pop('user_id', None)
    return redirect('/admin/')
@admin_blueprint.route('/adminmanual')
def adminmanual():
    return render_template('admin/adminmanual.html')




global_status = None

@admin_blueprint.route("/single/<string:post_slug>", methods=['GET'])
def single(post_slug):
    global global_status  # Declare the global variable
    if 'user_id' in session:
        data = Reservation.query.filter_by(id=post_slug).first()
        session['emails'] = data.email
        global_status = data.status  # Assign the status to the global variable
        return render_template('admin/adminorderdetail.html', data=data)
    else:
        return redirect('/admin/')

@admin_blueprint.route("/singles/<string:post_slug>",methods=['GET'])
def singles(post_slug):
    datas = Car.query.filter_by(id=post_slug).first()
    return render_template('admin/adminupdate.html', car=datas)


@admin_blueprint.route("/update_car/<int:car_id>", methods=['POST'])
def update_car(car_id):
    car = Car.query.get(car_id)

    if car:
        car.name = request.form.get('name')
        car.description = request.form.get('description')
        car.rent = request.form.get('rent')
        car.transmission = request.form.get('trans')
        car.fuel = request.form.get('fuel')
        car.color = request.form.get('color')
        car.type = request.form.get('type')
        car.engine = request.form.get('engine')
        car.ac = request.form.get('ac')
        car.capacity = request.form.get('capacity')
        car.b_name = request.form.get('b_name')
        # Handle the uploaded images
        images = request.files.getlist("images")
        image_filenames = []

        for image in images:
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filenames.append(filename)

        # Convert the list of image filenames to a comma-separated string
        image_filenames_str = ','.join(image_filenames)

        # Update the car's images in the database
        car.images = image_filenames_str

        db.session.commit()

        return redirect(url_for('admin.show_alert4', messages='Car details are updated'))

    return render_template('admin/update_car.html', car=car)

@admin_blueprint.route('/adminorder')
def reservations():
    if 'user_id' in session:
        data = Reservation.query.order_by(Reservation.id.desc()).all()
        return render_template('admin/adminorder.html', data=data)
    else:
        return redirect('/admin/')

@admin_blueprint.route('/update_status', methods=['POST'])
def update_status():
    data_id = request.form.get('data_id')
    new_status = request.form.get('new_status')

    data = Reservation.query.get(data_id)


    if data:
        data.status = new_status
        db.session.commit()


    return redirect('/admin/adminorder')




def send_email(message_body):
    # Create an SMTP connection using the App Password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, APP_PASSWORD)

    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = "CAR RENT"
    msg['To'] = session['emails']
    msg['Subject'] = 'Car Reservation'
    msg.attach(MIMEText(message_body, 'plain'))

    # Send the email
    server.sendmail(EMAIL_ADDRESS, session['emails'], msg.as_string())
    server.quit()

@admin_blueprint.route('/show_alerts/<messages>')
def show_alerts(messages):
    return render_template('admin/alert3.html', messages=messages)


@admin_blueprint.route('/confirm', methods=['POST'])
def confirm():
    global global_status  # Access the global variable
    if request.method == 'POST':
        if 'send_email' in request.form:
            message_body = f"Your Reservation is {global_status}"

            # Send the email
            send_email(message_body)
            return redirect(url_for('admin.show_alerts', messages='Email Sent To User'))
if __name__ == "__main__":
    app.run(debug=True)
