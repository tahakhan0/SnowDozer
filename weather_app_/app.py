import darksky
from flask import Flask, flash, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import time, psycopg2

app = Flask(__name__)
url_database = "Provide_your_database_credentials_here"
app.config['SQLALCHEMY_DATABASE_URI'] = url_database
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    coordinates_ = db.Column(db.String(100), nullable=False, unique=False)
    time_ = db.Column(db.String(120), nullable=True, unique=False)
    temp_ = db.Column(db.Float, nullable=True, unique=False)
    summary_ = db.Column(db.String(150), nullable=True, unique=False)
    percipitation_ = db.Column(db.Float, nullable=True, unique=False)
    Automated_on = db.Column(db.String(10), nullable=False, default="Turn On", unique=False)
    Pi_Turn_on = db.Column(db.String(10), nullable=False, default="Turn On", unique=False)
    pi_actual_status =  db.Column(db.String(10), nullable= True, unique=False )

    def __init__(self, coordinates_, time_, temp_, summary_, percipitation_,Automated_on, Pi_Turn_on,pi_actual_status):
        self.coordinates_ = coordinates_
        self.time_ = time_
        self.temp_ = temp_
        self.summary_ = summary_
        self.percipitation_ = percipitation_
        self.Automated_on = Automated_on
        self.Pi_Turn_on = Pi_Turn_on
        self.pi_actual_status = pi_actual_status

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST', 'GET'])
def success():
    global coords
    if request.method == 'POST':
        new_coordinates = request.form['Coordinates_html']
        check_coordinates = darksky.index(new_coordinates)
        if check_coordinates == 'Invalid':
            print('Enter coordinates again')
            return render_template('index.html')
    coords = new_coordinates
    weather_function=gather_data(coords)
    return render_template('success.html', myWeather=weather_function, user="Select an option",  pi_status= "Select an option" )


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        if request.form['submit-button'] == 'Automated':
            weather_function = gather_data(coords, Automated_on_obj='Turn On', Pi_turn_on_obj=None)
            return render_template('success.html', myWeather=weather_function, user="Automated", pi_status="Auto")
        if request.form['submit-button'] == 'Turn On':
            weather_function = gather_data(coords, Automated_on_obj='Turn Off', Pi_turn_on_obj='Turn On')
            return render_template('success.html', myWeather=weather_function, user="controlled by User", pi_status="On")
        weather_function = gather_data(coords, Automated_on_obj='Turn Off', Pi_turn_on_obj='Turn Off')
        return render_template('success.html', myWeather=weather_function,user="controlled by User", pi_status="off")


def gather_data(new_coordinates=None, Automated_on_obj=None, Pi_turn_on_obj=None, pi_actual_status_val = None):
    weather_data = []
    information = darksky.index(new_coordinates)
    weather_data.append(information)
    new_time_obj = information['time']
    new_summary_obj = information['icon']
    new_temp_obj = information['temperature']
    new_percipitation_obj = information['percipitation']
    Automated_functionality = Automated_on_obj
    Pi_functionality = Pi_turn_on_obj
    Pi_actual_functionality = pi_actual_status_val

    print('FUNCTION WORKS')
    try:
        data = Data(new_coordinates, new_time_obj, new_temp_obj, new_summary_obj, new_percipitation_obj, Automated_functionality, Pi_functionality, Pi_actual_functionality)
        db.session.add(data)
        db.session.commit()
        print('COMMITTED TO DATABASE')
        print('Running again')
    except IntegrityError:
        db.session.rollback()
        print('An IntegrityError was encountered')
    return weather_data

@app.route('/update_data')
def update_data():
    conn = psycopg2.connect(url_database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1")
    rows = cur.fetchall()
    if rows[0][8] != None:
        return jsonify(result = rows[0][8])
    else:
        return jsonify(result ="Not updated from the Pi")
    

if __name__ == '__main__':
    app.debug = True
    app.run()
