# **Team Harmony**
---

Site access: http://ec2-52-209-212-197.eu-west-1.compute.amazonaws.com:5050
## Overview
Team Harmony is a project that aims to use WiFi log data to accurately estimate the percentage occupancy of a given room on campus.

Additionally, it provides contextual information to the user by allowing user-submitted events to be logged, scheduled, and displayed on the building map when the event occurs.

## Setup
**Step 1:** -- Raw data files should be placed in their appropriate directories before beginning

Required files:
- CSIOccupancyReport.xlsx (/data/raw_ground/)
- timetable_sh1.csv, timetable_sh2.csv, timetable_sh3.csv, timetable_sh4.csv (/data/raw_timetable/)
- CSI WiFiLogs unzipped CSV files. **1053 in total** (/data/raw_wifi/CSI WiFiLogs/)

**Step 2:** -- A local mysql server with user=*'root'* and password=*'Harmony'*.

**Step 3:** -- *setup.py* file should be run from the project root directory

 - *setup.py* invokes each of the parsing scripts in turn (located in /parser/), outputting the relevant CSV files.
 - Additionally, it runs the */parser/db_create.py* file to set up the MySQL database, and the */parser/db_insert.py* file then carries out the appropriate insertions into the newly created database.
 - Once the data has been inserted into the database, */Model/train.py* is invoked to use the database data in order to generate 3 classifier files that will be used to make occupancy estimations.  These will be stored in */occupancyclassifier/pk1objects/*.

**Step 4:** -- Managing and tracking uploaded data

- Additional WiFi log files that are uploaded by the user will be saved for future reference in */data/raw_wifi/Uploaded_Data/Completed_Inserts/*
- Any errors that occur during the upload/insertion of WiFi data, or ground truth data will be logged to text files in */docs/Error_Reports/*, along with the time of attempted upload, and the name of the file that was uploaded (if appropriate).

## Using the site
- Once setup is complete, the user may access the site at the following URL:
  - localhost:5000/
- Accessing the **Home** page will allow the user to input a time and date for which they wish to see occupancies.  On form submission, they will be presented with a map indicating this.
- Accessing the **Events** page will allow the user to submit information about a new event to the database.  Enter an event for the current day and hour, save it, and view the map on the Home page to display the event.
- The **Data** page allows the user to add additional data to the database, and retrains the predictive model accordingly.  For WiFi log data, the file submitted must be a *CSV* file in the same format as the original files from which the database was constructed.  For ground truth data, simply fill out the provided form, and submit.

 

## Contributing
Andrew Sweeney - *asweeney@flatsurfer.pl*

Iwona Sarna - *iwona-sarna@ucdconnect.ie*

Kevin Fitzpatrick - *mastery414@gmail.com*

Michael McNulty - *michael.mc-nulty@ucdconnect.ie*
