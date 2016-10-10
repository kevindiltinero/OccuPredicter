from flask import Flask

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './data/raw_wifi/Uploaded_Data'

from app import views
