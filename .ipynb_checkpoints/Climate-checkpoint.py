import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify
################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/date<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/name<br/>"
        f"/api/v1.0/latitude<br>"
        f"/api/v1.0/longitude<br>"
        f"/api/v1.0/elevation<br>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query for the dates and precipitation values
    results =   session.query(hawaii_measurements.csv.date,prcp).\
                order_by(date).all()
    # Convert to list of dictionaries to jsonify
    prcp_date_list = []
    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)
    session.close()
    return jsonify(prcp_date_list)
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations = {}
    # Query all stations
    results = session.query(hawaii_stations.csv.station,name).all()
    for s,name in results:
        stations[s] = name
    session.close()
 
    return jsonify(stations)
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Get the last date contained in the dataset and date from one year ago
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    # Query for the dates and temperature values
    results =   session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_year_date).\
                order_by(Measurement.date).all()
    # Convert to list of dictionaries to jsonify
    tobs_date_list = []
    for date, tobs in results:
        new_dict = {}
        new_dict[date] = tobs
        tobs_date_list.append(new_dict)
    session.close()
    return jsonify(tobs_date_list)

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
    """TMIN, TAVG, and TMAX per date starting from a starting date.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        end (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return_list = []

    results = session.query(  Measurement.date,\
                                func.min(Measurement.tobs), \
                                func.avg(Measurement.tobs), \
                                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        group_by(Measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["TMIN"] = min
        new_dict["TAVG"] = avg
        new_dict["TMAX"] = max
        return_list.append(new_dict)
    session.close()    
    return jsonify(return_list)
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
petsEngine = create_engine('postgresql://postgres:Theophile23@localhost:5432/pet_stuff')
Base = automap_base()
Base.prepare(petsEngine, reflect=True)
Pets = Base.classes.pets
app = Flask(__name__)
@app.route('/')
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my Home page!"
@app.route('/about')
def about():
    print("Server received request for jsonified 'About' page...")
    return jsonify([{"Hello": "World!"}, {"Another": "Dict!"}])
@app.route('/hi/<my_name>')
def hi(my_name):
    print("Server received request for 'Hi' page... Saying hi to" + my_name)
    return f"<h1>Hi {my_name}!</h1>"
@app.route('/add/<a>/<b>/<as_type>')
def add(a, b, as_type):
    print(f"Server received request for 'Add' page... Adding {a} + {b}")
    if as_type == 'str':
        response = a + b
    elif as_type == 'int':
        response = str(int(a) + int(b))
    elif as_type == 'float':
        response = str(float(a) + float(b))
    else:
        response = 'IDK...'
    return response
@app.route('/get_pets/<pet_names>')
def getPets(pet_names):
    print(f"Trying to get {pet_names} from pets table")
    try:
        session = Session(petsEngine)
        results = session.query(Pets).filter(Pets.pet_name.in_(pet_names.split(','))).all()
        response = [{'name': pet.pet_name, 'age': pet.pet_age} for pet in results]
    except Exception as e:
        response = 'Something broke... ' + str(e)
    return jsonify(response)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5007)