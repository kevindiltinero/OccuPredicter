import os

from flask import render_template, flash, redirect, request, url_for
from werkzeug.utils import secure_filename
from app import app

from views_utils import add_timestamp, allowed_file, parse_timestamp_csv, update_timestamp_db

UPLOAD_FOLDER = '/Users/Iwonka/Desktop/Timetable/timetable_webapp/upload'#the path to the folder where we uploaded files
ALLOWED_EXTENSIONS = set(['csv'])


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])#the GET method - download, POST - sending
def upload():
    if request.method == 'POST': #if the page is in the sending
        if 'file' not in request.files:# Check whether the file was sent
            flash('No file part')
            return redirect(request.url)

        fileobj = request.files['file']

        if fileobj.filename == '': #check if sent file is not empty
            flash('No selected file')
            return redirect(request.url)

        if fileobj and allowed_file(fileobj.filename):#check whether a file has good extension
            filename_timestamp = add_timestamp(fileobj.filename)
            filename = secure_filename(filename_timestamp)
            fileobj.save(os.path.join(UPLOAD_FOLDER, filename))#save the file to disk
            return redirect(url_for('upload_success', filename=filename))
    return render_template("upload.html")#if the site is in download mode displays the form for uploading files


@app.route('/uploaded', methods=['GET', 'POST'])
def upload_success():
    if 'filename' in request.args: #check whether the file uploaded by the argument
        filename = os.path.join(UPLOAD_FOLDER, request.args['filename']) #load the file forwarded by the argument
        timestamp = parse_timestamp_csv(filename) #parse file
        updated_rows = update_timestamp_db(timestamp) #update database based on the data from the file

    return render_template("upload_success.html", updated_rows=updated_rows) #display HTML


