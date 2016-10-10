from app import app
import calendar
from flask import g, render_template, request, redirect
import MySQLdb
import sqlite3
from time import mktime
from wtforms import Form, SelectField, StringField, BooleanField, TextAreaField, validators
import json
from werkzeug import secure_filename
import os
import random
import numpy as np
import pickle
import datetime
import matplotlib.pyplot as plt



########################  Database Connection  #################################

@app.before_request
def db_connect():
        g.db_conn = MySQLdb.connect(host='localhost', user='root', passwd='Harmony', db='Harmony_Data_Test')

@app.teardown_request
def db_disconnect(exception=None):
        g.db_conn.close()



#########################  Required Functions  #################################

# Load the serialised pickle classifier
clf = pickle.load(open('occupancyclassifier/pk1objects/occupancyclassfier.pk1', 'rb'))

# Also load classifiers for cases when certain data is not available
clf2 = pickle.load(open('occupancyclassifier/pk1objects/occupancyclassfier2.pk1', 'rb'))
clf3 = pickle.load(open('occupancyclassifier/pk1objects/occupancyclassfier3.pk1', 'rb'))

# THE WTFORMS
# These classes are forms, attributes are the various controls you can call upon (dropdown/text)
# You can change the fields

class HelloForm(Form):
    # Building selection on home page
    building = SelectField(u'Building', choices=[('Computer Science', 'Computer Science'), ('Science Hub', 'Science Hub')])
    
    # Month selection on home page
    month = SelectField(u'Month', choices=[('1', 'January'), ('2', 'February'), ('3', 'March'),
        ('4', 'April'), ('5', 'May'), ('6', 'June'),
        ('7', 'July'), ('8', 'August'), ('9', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')]) 

    # Year selection on home page
    year = SelectField(u'Year', choices=[('2015', '2015'), ('2016', '2016')])

    # Hour selection on home page
    hour = SelectField(u'Hour', choices=[('0', '09:00'), ('1', '10:00'), ('2', '11:00'), ('3', '12:00'),
        ('4', '13:00'), ('5', '14:00'), ('6', '15:00'), ('7', '16:00')])

    # Day selection on home page
    day = SelectField(u'Day', choices=[('1', '1st'), ('2', '2nd'), ('3', '3rd'),
                                            ('4', '4th'), ('5', '5th'), ('6', '6th'),
                                            ('7', '7th'), ('8', '8th'), ('9', '9th'),
                                            ('10', '10th'), ('11', '11th'), ('12', '12th'),
                                            ('13', '13th'), ('14', '14th'), ('15', '15th'),
                                            ('16', '16th'), ('17', '17th'), ('18', '18th'),
                                            ('19', '19th'), ('20', '20th'), ('21', '21st'),
                                            ('22', '22nd'), ('23', '23rd'), ('24', '24th'),
                                            ('25', '25th'), ('26', '26th'), ('27', '27th'),
                                            ('28', '28th'), ('29', '29th'), ('30', '30th'), ('31', '31st')])
    # Day selection on events page
    sayhello = SelectField(u'Day', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                                            ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
                                            ('Sunday', 'Sunday')])
    # Hour selection on events page
    saygoodbye = SelectField(u'Hour', choices=[('00', '00'),('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),('06', '06'),('07', '07'),('08', '08'),('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'),
                                               ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),('21', '21'),('22', '22'),('23', '23') ])

    # Event type
    event = SelectField(u'Event', choices=[('cancel', 'Cancellation'), ('talk', 'Talk'), ('exam', 'Exam'),
                                           ('study', 'Study Group')])
    # Room selection on events page
    room = SelectField(u'Hour', choices=[('Computer Science', 'Computer Science'), ('Science Hub', 'Science Hub')])
	
    slice = SelectField(u'Room', choices=[('B1178', 'B1.17/8'), ('E1.19', 'E1.19'), ('E1.32', 'E1.32'), ('E1.33', 'E1.33'),
                                         ('E1.34', 'E1.34'), ('E1.43', 'E1.43'), ('E1.44', 'E1.44'),
                                         ('E1.45', 'E1.45'), ('E1.52', 'E1.52'), ('E1.53', 'E1.53'), ('E1.55', 'E1.55'),
                                         ('E1.56', 'E1.56'), ('E1.52', 'E1.52'), ('B0.02', 'B0.02'), ('B0.03', 'B0.03'),
                                         ('B0.04', 'B0.04'), ('B1.09', 'B1.09'), ('B1.08', 'B1.08'), ('B1.06', 'B1.06')
                                         ])
										 
    # Event description
    description = TextAreaField('Describe The Event', [validators.DataRequired()])

    # Add extra information
    extra = BooleanField('Add contextual Info', [validators.DataRequired()])

# Use the datetime module to get the current day and hour
def check_time():
    #Get the current hour and date
    time = str(datetime.datetime.now())
    hour = time[11:13]
    my_date = datetime.date.today()
    day = calendar.day_name[my_date.weekday()]
    return [day, hour]

# MATRIX GENERATOR FOR THE CLASSIFIER
# This function creates the matrix(nested list) that the classifier will predict like so:
# day/time from checktime() are it's parameters, selects every row from ABT with that time/day,
# The values within the row are excluded unless they correspond to our descriptive features the model expects
# ULTIMATELY- Outputs nested list that includes rooms and their predicted occupancies 

def select_from(day, month, year, hour, building):

    # Connect and declare cursor
    g.db_conn = MySQLdb.connect(host='localhost', user='root', passwd='Harmony', db='Harmony_Data_Test')
    c = g.db_conn.cursor()
    
    # We get the day of the month in as an integer, so use datetime to pick out the weekday
    # Then convert the weekday to the encoded value for the abt
    # Hour must be + 9, as encoded values range from 0-7 to represent 9am-4pm
    dt = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour)+9)

    # Get the weekday as an integer
    weekday = dt.weekday()

    # Create a timestamp for later use
    unix_time = int(mktime(dt.timetuple()))

    # First retrieve a list of rooms for the current building
    query = "SELECT room_id FROM room WHERE building = '" + building + "'"
    c.execute(query)
    r = c.fetchall()

    # Use list comprehension to extract these room names
    string_rooms = [x[0] for x in list(r)]

    # Numerical representation of the rooms for accessing encoded ABT
    room_list = range(len(string_rooms))

    # Final list to house predictions paired with rooms
    all_room_results = []

    # One query for each room
    # Different data might be available for different rooms
    for j in room_list:

        # Will fail if wifi data does not exist for that day, in which case we must use another classifier
        # Best scenario, where we have Wifi log data, and timetable data
        c.execute("SELECT Module, Room, Registered, Authenticated, Associated "
                  "FROM abt "
                  "WHERE Day = %s AND Month = %s AND Year = %s AND Time = %s AND Room = %s", (weekday, month, year, hour, j))
        results = c.fetchall()

        # If there is data returned from the query, extract the relevant integers corresponding to the ABT
        # Add them in the correct order to a list for running through the model
        if len(results) != 0:
            mod = int(results[0][0])
            room = int(results[0][1])
            reg = int(results[0][2])
            auth = int(results[0][3])
            assoc = int(results[0][4])

            # Predict using the decision tree classifier
            # Store prediction and room number in a list
            clf_prediction = clf.predict([mod, room, reg, auth, assoc])
            all_room_results.append(int(clf_prediction))

        # No wifi data available
        # Information we need ['Month', 'Capacity', 'Type', 'Registered']
        else:

            # Dictionary constructed manually from iPython notebook
            # Allows mapping between module codes and the integers they are encoded as in the ABT
            module_codes = {
                    'COMP30190': 15, 'COMP10280': 2, 'COMP47300': 27, 'STAT40150': 32,
                    'COMP40370': 21, 'COMP20020': 4, 'COMP30250': 18, 'COMP30120': 13,
                    'COMP41690': 25, 'not available': 33, 'SCI30060': 31, 'COMP30060': 9,
                    'COMP40660': 22, 'MATH10200': 30, 'COMP30080': 11, 'COMP30520': 20,
                    'ENVB30110': 28, 'MATH10130': 29, 'COMP20010': 3, 'COMP20130': 7,
                    'COMP30110': 12, 'COMP20110': 6, 'COMP30070': 10, 'COMP20070': 5,
                    'COMP30240': 17, 'COMP30010': 8, 'COMP30170': 14, 'COMP30260': 19,
                    'COMP41110': 23, 'COMP30220': 16, 'COMP47290': 26, 'COMP10130': 1,
                    'COMP10110': 0, 'COMP41450': 24}

            # Create a simple dictionary for mapping integers to class types
            type_dict = {'Classroom':0, 'Lecture Theatre':1, 'A.L.E.':2, 'Seminar':3}

            # Execute a query to get the data required (Module, Registered, Room)
            # There is no information for rooms other than B002, B003, and B004 in the ABT
            # Therefore, must use other tables
            query = "SELECT type, capacity FROM room WHERE room_id = '" + string_rooms[j] +"'"
            c.execute(query)
            results = c.fetchall()
            cap = results[0][1]
            room_type = results[0][0]

            # Now we need to get the number of registered students
            # Must be for the class taking place at the input time, for the current room
            query = "SELECT m.total_students FROM module m join class c on m.code = c.code WHERE c.timestamp = " + str(unix_time) + " AND c.room_id = '" + string_rooms[j] + "'"
            c.execute(query)
            reg = c.fetchall()

            # If the seconday query is successful
            # Convert all data to encoded integers, and add to a list
            if len(reg) != 0 and len(room_type) != 0 and len(cap) != 0:
                clf2_prediction = clf2.predict([month, int(cap), type_dict[room_type], int(reg)])
                all_room_results.append(int(clf2_prediction))


            # If none of the previous queries return results
            # We must use the only information available
            # According to our iPython notebook analysis, the best feature combination for this situation is
            # ["Day", "Month", "Capacity", "Type"]
            else:
                try:
                    # Query database using the third set of features determined from model evaluation
                    query = "SELECT capacity, type FROM room WHERE room_id = '" + string_rooms[j] +"'"
                    c.execute(query)
                    results = c.fetchall()
                    if len(results) != 0:
                        cap = int(results[0][0])
                        room_type = type_dict[results[0][1]]
                        clf3_prediction = clf3.predict([weekday, month, cap, room_type])
                        all_room_results.append(int(clf3_prediction))

                except:
                    print "Need to generate example values, as none is currently available for J =", j
                    all_room_results.append(2)

    if len(all_room_results) == 0:
        all_room_results = [1,2,3,1,2,3]

    hub_values = [random.sample(range(0,5), 1)[0] for x in range(12)]

    return [all_room_results, hub_values]


# Form to write events into the events table
def war_writting(day, hour, room, event, description):
    # Set up the connection.
    c = g.db_conn.cursor()
    ## Write ABT into the Database
    description = str(description).strip()

    # Must convert everything to strings, as WTForms returns in unicode
    c.execute('INSERT INTO eventsx (datey, hour, room, event, description)'\
              'VALUES (%s, %s, %s, %s, %s)', (str(day), str(hour), str(room), str(event), str(description)))
    g.db_conn.commit()

# This checks if there is any events that need to be plotted with the icons
# It checks it by seing if day and time match the current day time
def war_checking(day, hour):
    # Setup the cursor
    c = g.db_conn.cursor()
    dayofweek = day
    hourofday = hour
    command = "SELECT * FROM eventsx WHERE datey = '"+dayofweek+"' AND hour = '"+hourofday+"'"
    c.execute(command)
    results = c.fetchall()

    ### MAP the room slices that are to be shown
    if results:
        eventpicture_mapping = {'study': 'meet.jpg', 'talk': 'speech.jpg', 'cancel': 'cancel.jpg',
                                'exam': 'exam.jpg'}
        # Change the rooms to slices when sending the info back.
        slices = []
        for row in results:
        #     Get all the slices by clever nested indexing, event and description are with it
        #     # Event is to change picture, description written to box, slice to make visible.
            slices.append([row[2], eventpicture_mapping[row[3]], row[4], row[3]])
        return slices
    else:
        return -1

# Specify the types of files that are allowed
# Only CSVs for Wifi Logs
ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    """ Checks that a file has an extension, and that it is allowed """
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS



##########################  Basic Page Views  ##################################

# Welcome Page
#==================
@app.route('/')
@app.route('/welcome')
@app.route('/index')
def welcome():
        return render_template("welcome.html", title="Welcome") 

# Data Upload Page
#==================
@app.route('/data')
def data():
    return render_template('data.html', title="Data")

#Modules Page
#==================
@app.route('/modules', methods = ['GET', 'POST'])
def modules():
    if request.method == 'POST':
        module = str(request.form.get('code'))
	
	# Connect to the database
        c = g.db_conn.cursor()

	# Select number of registered students for that module
        c.execute("SELECT total_students FROM module WHERE code = %s", (module,))
        # return this data
        result = c.fetchone()
        students = result[0]

	# Select locations for that module
        c.execute("SELECT room_id FROM class WHERE code = %s", (module,))
        # return this data
        result = c.fetchone()
        room = result[0]
	
        # Select time for that module
        c.execute("SELECT timestamp FROM class WHERE code = %s", (module,))
        # return this data
        result = c.fetchone()
        timestamp  = result[0]	
	#mydate = datetime.fromtimestamp(timestamp) #convert unix timestamp to datetime object
	#time = datetime.mydate.strftime('%H:%M')
	#day = datetime.datetime.mydate #returns weekday as integer
	#days=["Monday","Tuesday","Wednesday","Thursday","Friday"]
	#myday = days[day]

	return render_template("modules.html", module=module, students=students, room=room, time='13.00', myday='Tuesday', title="Modules")
    else:
	return render_template("modules.html", title="Modules")

# Rooms Page
#==================
@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        room = str(request.form.get('room'))
	
    	# Connect to the database
	c = g.db_conn.cursor()

	# Select the room type
	c.execute("Select type from room where room_id = %s", (room,))
	#return the data
	result = c.fetchone()	
	b_type = ''.join(result)

	# Select the building
        c.execute("Select building from room where room_id = %s", (room,))
        #return the data
	result = c.fetchone()	
        building = ''.join(result)
	
	# Select the capacity
        c.execute("Select capacity from room where room_id = %s", (room,))
        #return the data
	result = c.fetchone()	
	capacity = result[0]

	# Select 0% percentage occupied for that room
	c.execute("SELECT COUNT(occupancy) FROM survey WHERE room_id = %s AND occupancy = '0'", (room,))
	# return this data
	result = c.fetchone()
	int0 = result[0]
 
	# Select 25% percentage occupied for that room
	c.execute("SELECT COUNT(occupancy) FROM survey WHERE room_id = %s AND occupancy = '25'", (room,))
	# return this data
	result = c.fetchone()
	int25 = result[0]
	
	# Select 50% percentage occupied for that room
	c.execute("SELECT COUNT(occupancy) FROM survey WHERE room_id = %s AND occupancy = '50'", (room,))
	# return this data
	result = c.fetchone()
	int50 = result[0]
	
	# Select 75% percentage occupied for that room
	c.execute("SELECT COUNT(occupancy) FROM survey WHERE room_id = %s AND occupancy = '75'", (room,))
	# return this data
	result = c.fetchone()
	int75 = result[0]
	
	# Select 100% percentage occupied for that room
	c.execute("SELECT COUNT(occupancy) FROM survey WHERE room_id = %s AND occupancy = '100'", (room,))
	# return this data
	result = c.fetchone()
	int100 = result[0]
	
	# Create a list of % occupied from 0 to 100
	mylist = [int0, int25, int50, int75, int100]

    	return render_template("rooms.html", room=room, b_type=b_type, building=building, capacity=capacity, mylist=mylist, title="Rooms")
    else:
    	return render_template("rooms.html", title="Rooms")

# Home Page
#==================
@app.route('/home', methods=['GET', 'POST'])
def home():
    
    # Get the time with the time checker app
    time_info = check_time()

    # Check if there are events to be plotted
    pull_events = war_checking(time_info[0], time_info[1])
    
    # Assign temporary values
    fake = [[0, 2, 1, 1, 2, 0], [0, 2, 1, 1, 2, 0, 2, 4, 3, 2, 3, 3]]

    # When the page is first loaded, there is no form submission, so create default
    if request.method == "GET":
        form = HelloForm(day=2, month=11, year=2015, hour=0)

        # The .data attribute allows us to get the value submitted in the form rather than the explicit HTML code
        day = form.day.data
        month = form.month.data
        year = form.year.data
        hour = form.hour.data

        return render_template('home.html', values=fake, events=pull_events, form=form)

    # Once a form is submitted we can return the predictions for the given map
    if request.method == "POST":
        form = HelloForm(request.form)
        day = form.day.data
        month = form.month.data
        year = form.year.data
        hour = form.hour.data
        building = form.building.data


    # Make the matrix with our function
    # Building is input to get the rooms that are part of that building
    # This will return a 2-dimensional list, where each sublist contains a room and its predicted occupancy
    matrix_values = select_from(int(day), int(month), int(year), int(hour), str(building))

    return render_template('home.html', values=matrix_values, events=pull_events, form=form, day=day, room=building, matrix=matrix_values)

# Events Page
#==================
@app.route('/events', methods=['POST', 'GET'])
# This is simply the rendering of the page from the navigation bar. See form functionality below.
def events():
    form = HelloForm(request.form)
    return render_template('events.html', form=form)


##########################  Functional URLs  ###################################

# Allow a user-uploaded file to be processed, saved, and inserted into the database
@app.route('/upload', methods=["POST"])
def upload_file():
    """ Parses uploaded file and inserts into database """
    # Get the FileStorage object that was uploaded
    file = request.files["file"]
    # If no file was uploaded, return to upload page with error message
    if file.filename == "":
        return render_template('data.html', title="Data", data=["false", "wifi"])
    # Otherwise check that there is a file, and that the filename is of the correct type
    if file and allowed_file(file.filename):
        # Get the raw filename
        filename = secure_filename(file.filename)
        # Save it to the specified directory
        file_dir = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_dir)
        from parser import wifi_parser
        from parser import db_insert
        # Now parse the file, and write it to a temporary csv
        cleaned_dataframe = wifi_parser.parse_wifi(file_dir)
        wifi_parser.write_wifi(cleaned_dataframe, os.path.join(app.config["UPLOAD_FOLDER"], "parsed.csv"))
        try:
            db_insert.db_write_wifi(os.path.join(app.config["UPLOAD_FOLDER"], "parsed.csv"))
        except:
            print """
            #########################
            error writing to database
            #########################
            """
            return render_template('data.html', title="Data", data=["false", "wifi"])
        # Move the completed file to the appropriate directory
        os.rename(file_dir, os.path.join(app.config["UPLOAD_FOLDER"], "Completed_Inserts", filename)) 

        try:
            # Remove the temporary csv file
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], "parsed.csv"))
        except:
            print """
            ###############
            file deletion failed
            ###############
            """
            return render_template('data.html', title="Data", data=["false", "wifi"])

        return render_template("data.html", title="Data", data=["true", "wifi"])

    # Wrong filetype submitted
    else:
        return render_template('data.html', title="Data", data=["false", "wifi"])
    
# Processing uploaded Ground Truth data
@app.route('/surveyupload', methods=["POST"])
def survey_upload():

    try:
        room = request.form["room_input"]
        is_occupied = int(request.form["is_occupied"])
        occupancy = int(request.form["occupancy"])
        year = int(request.form["year"])
        month = int(request.form["month"])
        day = int(request.form["day"])
        hour = int(request.form["time"])

        dt = datetime.datetime(year=year, month=month, day=day, hour=hour)
        unix_time = int(mktime(dt.timetuple()))

        c = g.db_conn.cursor()
        # Attempt to log data to database
        # Will fail if an entry for that room at that time exists
        try:
            c.execute("INSERT INTO survey(room_id, occupied, occupancy, timestamp) VALUES (%s, %s, %s, %s)", (room, is_occupied, occupancy, unix_time))
            g.db_conn.commit()
            return render_template("data.html", title="Data", data=["true", "ground"])

        # If something fails, render template with failure message, and log failure to text file
        except:
            with open("./docs/Error_Reports/ground_insert_errors.txt", "a") as f:
                f.write(str(datetime.datetime.now().strftime("%d-%m-%Y @ %H:%M:%S"))+"\nValues: ['room_id': "+str(room)+", 'occupied': "+str(is_occupied)+", 'occupancy': "+str(occupancy)+", 'timestamp': "+str(unix_time)+"]")

            print "An error occurred. Details logged to './docs/Error_Reports/ground_insert_errors.txt'."

            # Return the template with the error message
            return render_template("data.html", title="Data", data=["false", "ground"])

    except:
        return render_template("data.html", title="Data", data=["false", "ground"])

# EVENTS FORM
# Gets the data that they input into the events form and writes it into the events table
@app.route('/hello', methods=['POST'])
def hello():
    form = HelloForm(request.form)
    if request.method == 'POST':
        event = request.form['event']
        day = request.form['sayhello']
        hour = request.form['saygoodbye']
        room = request.form['slice']
        descr = request.form['description']
        war_writting(day, hour, room, event, descr)
        return render_template('events.html', form=form)

@app.route('/clear')
def clearevents():

    form = HelloForm(saygoodbye="9", sayhello="Monday")
    c = g.db_conn.cursor()

    # datey must be a string, so this workaround drops everything
    c.execute("DELETE FROM eventsx WHERE datey <> 'asdfg'")
    g.db_conn.commit()
    return render_template('events.html', form=form)

