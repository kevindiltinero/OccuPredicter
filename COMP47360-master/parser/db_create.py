import MySQLdb

def create_db():

    # Ask the user to confirm the overwrite of an existing database
    confirm = raw_input("Data is going to be written to the following database: 'Harmony_Data_Test'.\nThis will overwrite the database if it already exists.\nAre you sure you wish to continue? [Y/N] ")


    # Ask again if an invalid response is provided
    while confirm.upper() != "Y" and confirm.upper() != "N":
        print "Invalid response. Please try again."
        confirm = raw_input("Data is going to be written to the following database: 'Harmony_Data_Test'.\nThis will overwrite the database if it already exists.\nAre you sure you wish to continue? [Y/N] ")


    # If use allows database overwrite
    if confirm.upper() == "Y":
        print "Connecting to MySQL..."
        db_conn = MySQLdb.connect(host="localhost", user="root", passwd="Harmony")
        print "Connection successful."
        c = db_conn.cursor()

        print "Creating database..."

        try:
            c.execute("DROP DATABASE Harmony_Data_Test")
            print "Overwriting existing database."
        except:
            print "Creating new database."

        c.execute("CREATE DATABASE IF NOT EXISTS Harmony_Data_Test")
        c.execute("USE Harmony_Data_Test")
        print "Database creation successful."

        print "Creating tables..."
        c.execute("""CREATE TABLE room (
        room_id VARCHAR(45) PRIMARY KEY,
        capacity INT(11),
        type VARCHAR(45),
        building VARCHAR(45))""")

        c.execute("""CREATE TABLE wifi (
        record_id INT(11) PRIMARY KEY AUTO_INCREMENT,
        room_id VARCHAR(45),
        timestamp INT(11),
        authenticated INT(11),
        associated INT(11),
        UNIQUE time_room (timestamp, room_id),
        FOREIGN KEY wifi(room_id) REFERENCES room(room_id))""")

        c.execute("""CREATE TABLE survey (
        survey_id INT(11) PRIMARY KEY AUTO_INCREMENT,
        room_id VARCHAR(45),
        timestamp INT(11),
        occupied BOOLEAN,
        occupancy INT(11),
        UNIQUE room_time (timestamp, room_id),
        FOREIGN KEY survey(room_id) REFERENCES room(room_id))""")

        c.execute("""CREATE TABLE module (
        code VARCHAR(45) PRIMARY KEY,
        total_students INT(11))""")

        c.execute("""CREATE TABLE class (
        room_id VARCHAR(45),
        timestamp INT(11),
        code VARCHAR(45),
        PRIMARY KEY (room_id, timestamp, code),
        FOREIGN KEY class(code) REFERENCES module(code),
        FOREIGN KEY class(room_id) REFERENCES room(room_id))""")

        c.execute("""CREATE TABLE eventsx (
        datey VARCHAR(45),
        hour VARCHAR(45),
        room VARCHAR(45),
        event VARCHAR(45),
        description VARCHAR(256),
        PRIMARY KEY (datey, hour, room))""")

        db_conn.commit()
        print "Tables created successfully."

    # User chose to not overwrite database. Program exits.
    else:
        raise IOError("Database overwrite declined.")

if __name__ == "__main__":
    create_db()
