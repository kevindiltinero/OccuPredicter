import datetime, time
import pandas as pd
from flask import flash
from app import db, models

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def add_timestamp(filename):
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) #formatting of today's date on the numerical timestamp
    splited = filename.split('.')
    return "{0}_{1}.{2}".format("".join(splited[:-1]), timestamp, splited[-1])


def parse_timestamp_csv(filename):
    return pd.read_csv(filename)


def update_timestamp_db(timestamp):
    all_models = db.session.query(models.Clas).all() #download all data from db
    for model in all_models:
        db.session.delete(model) #remove the object from the database
    db.session.commit()#confirm the action on the database

    for header in ["room_id", "timestamp", "code"]:#check that all the columns are in the file
        if header not in list(timestamp):  # missing column:
            flash("Wrong file format. Missing column: {0}.".format(header))
            return 0

    for _, row in timestamp.iterrows(): #for each line in the file create a new file and add it to the database
        room_id = row["room_id"]
        timestamp = row["timestamp"]
        code = row["code"]

        #clas_models.filter_by(room_id=room_id, code=code, timestamp=timestamp).all()  #checks whether this object exists
        model = models.Clas(room_id=room_id, timestamp=timestamp, code=code)
        db.session.add(model)
    db.session.commit()

    return len(db.session.query(models.Clas).all())



