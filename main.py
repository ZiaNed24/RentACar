from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint
main_blueprint = Blueprint('main', __name__)
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/rentacar'  # Replace with your database details
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = secrets.token_hex(24)  # You can adjust the key length as needed

# Set the secret key for your Flask application
app.secret_key = secret_key  # Set a strong secret key
def create_app(app):
    db.init_app(app)

@main_blueprint.route('/show_alert/<message>')
def show_alert(message):
    return render_template('main/alert.html', message=message)
    return redirect('/')

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    images = db.Column(db.String(100))
    rent = db.Column(db.String(100))
    transmission = db.Column(db.String(100))
    capacity = db.Column(db.String(100))
    type = db.Column(db.String(100))
    fuel = db.Column(db.String(100))
    color = db.Column(db.String(100))
    engine = db.Column(db.String(100))
    ac = db.Column(db.String(100))
    b_name = db.Column(db.String(100))

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),  nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50),  nullable=False)
    lname = db.Column(db.String(50),  nullable=False)
    email = db.Column(db.String(100), nullable=False)
    msg = db.Column(db.String(100), nullable=False)
    p_num = db.Column(db.String(100), nullable=False)

@main_blueprint.route('/')
def index():
    tasks = Login.query.all()
    return render_template('main/login.html', tasks=tasks)

@main_blueprint.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    phone = request.form['phone']
    new_task = Login(name=name, email=email, password=password, address=address, phone=phone)
    db.session.add(new_task)
    db.session.commit()
    flash('User registered successfully', 'success')
    return redirect(url_for('main.index'))

@main_blueprint.route('/contact', methods=['POST'])
def contact():
    fname = request.form['firstname']
    lname = request.form['lastname']
    email = request.form['email']
    p_num = request.form['phone']
    msg = request.form['msg']
    new_task = Contact(fname=fname, lname=lname, email=email, p_num=p_num, msg=msg)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.contacts'))

@main_blueprint.route('/')
def home():
    return render_template('main/login.html')

@main_blueprint.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Login.query.filter_by(email=email, password=password).first()

    if user:
        # Login successful, store the user ID in the session
        session['user_id'] = user.id
        session['name'] = user.name
        session['email'] = user.email
        session['phone'] = user.phone
        return redirect('/index1')
    else:
        return redirect(url_for('show_alert', message='Login failed'))
        return redirect('/')


@main_blueprint.route('/logout')
def logout():
    # Clear the user ID from the session on logout
    session.pop('user_id', None)
    return redirect('/')




@main_blueprint.route("/index1")
def index1():
    if 'user_id' in session:
        tasks = Car.query.all()
        return render_template("main/index.html", tasks=tasks)

    else:
        return redirect('/')


@main_blueprint.route("/about")
def about():
    return render_template("main/about.html")

@main_blueprint.route("/single/<string:post_slug>",methods=['GET'])
def single(post_slug):
    post=Car.query.filter_by(id=post_slug).first()
    session['img'] = (post.images.split(',')[0])
    session['cname'] = post.name
    session['cname'] = post.name
    session['rent'] = post.rent
    return render_template("main/car_details.html",post=post)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_locat = db.Column(db.String(50),  nullable=False)
    d_locat = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    passengers = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    fuel = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    driver = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    cname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

@main_blueprint.route("/contacts")
def contacts():
    return render_template("main/contact.html")

@main_blueprint.route("/reser")
def reser():

    return render_template("main/reservation.html")


@main_blueprint.route('/register_car', methods=['POST'])
def register_car():
    p_locat = request.form['location1']
    d_locat = request.form['location2']
    date = request.form['date']
    passengers = request.form['passengers']
    color = request.form['color']
    fuel = request.form['fuel']
    model = request.form['model']
    driver = request.form['driver']
    name=session['name']
    email=session['email']
    phone=session['phone']
    cname=session['cname']
    status='pending'
    new_task = Reservation(status=status,cname=cname,name=name,phone=phone,email=email,p_locat=p_locat, d_locat=d_locat, date=date, passengers=passengers, color=color,fuel=fuel,model=model,driver=driver)
    session['p_lo'] = new_task.p_locat
    session['name'] = new_task.name
    session['d_lo'] = new_task.d_locat
    session['date'] = new_task.date
    session['pass'] = new_task.passengers
    session['color'] = new_task.color
    session['fuel'] = new_task.fuel
    session['model'] = new_task.model
    session['driver'] = new_task.driver

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('main.reser'))
@main_blueprint.route("/single")
def single1():
    return render_template("main/car_details.html")
@main_blueprint.route("/cars")
def cars():
    if 'user_id' in session:
        tasks = Car.query.all()
        return render_template("main/gallery.html", tasks=tasks)

    else:
        return redirect('/')





EMAIL_ADDRESS = 'zianawaz43210@gmail.com'  # Replace with your Gmail email
APP_PASSWORD = 'vuph iccj kltm lsrh'  # Replace with the App Password

def send_email(message_body):
    # Create an SMTP connection using the App Password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, APP_PASSWORD)

    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = "CAR RENT"
    msg['To'] = session['email']
    msg['Subject'] = 'Car Reservation'
    msg.attach(MIMEText(message_body, 'plain'))

    # Send the email
    server.sendmail(EMAIL_ADDRESS, session['email'], msg.as_string())
    server.quit()

@main_blueprint.route('/show_alerts/<messages>')
def show_alerts(messages):
    return render_template('main/alert2.html', messages=messages)


@main_blueprint.route('/confirm', methods=['POST'])
def confirm():
    if request.method == 'POST':
        if 'send_email' in request.form:
            message_body = f"You are selected {session['cname']},\n\nWhich color is {session['color']} with {session['fuel']},{session['model']} model,{session['driver']} .\nHaving Capacity of {session['pass']}.\n\nFrom {session['p_lo']} to {session['d_lo']}\nat {session['date']}\n\nAfter check your demands we will contact you soon "
            # Send the email
            send_email(message_body)
            return redirect(url_for('main.show_alerts', messages='Your Car Is Registered. Please Check Your Email'))

if __name__ == "__main__":
    app.run(debug=True)
