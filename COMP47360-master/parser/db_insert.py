import pandas as pd
import MySQLdb
import datetime

def db_write_wifi(csv):

    # Load csv into dataframe
    df = pd.read_csv(csv, engine="python")
    # Convert every pandas row to a tuple, ignoring the index
    # Store all tuples in a list
    list_to_insert = [tuple(x) for x in df.ix[:,1:].to_records(index=False)]

    # Connect to database and establish cursor
    db_conn = MySQLdb.connect(host='localhost', user='root', passwd='Harmony', db='Harmony_Data_Test')
    c = db_conn.cursor()
    for i in list_to_insert:
        room = i[0]
        time = int(i[1])
        assoc = int(i[2])
        auth = int(i[3])

        # Attempt to insert the data
        # There can only be one entry for a particular room at a given time
        # So if a timestamp already exists, log to file
        try:
            c.execute("INSERT INTO wifi(room_id, timestamp, associated, authenticated) VALUES (%s, %s, %s, %s)", (room, time, assoc, auth))
        except:
            with open("./docs/Error_Reports/wifi_insert_errors.txt", "a") as f:
                f.write(str(datetime.datetime.now().strftime("%d-%m-%Y @ %H:%M:%S"))+"\nFrom file: "+csv+"\nValues: "+str(i)+"\n\n")
            print "An error occurred. Details logged to './docs/Error_Reports/wifi_insert_errors.txt'."

    db_conn.commit()
    return True

def insert_ground_data():
	
	df = pd.read_csv("./data/Cleaned_Data/Cleaned_Ground_Data.csv", engine="python", index_col=0, names=["a", "b", "c", "d", "e", "f", "g", "h"])
        list_to_insert = [tuple(x) for x in df.to_records()]
	
	db_conn=MySQLdb.connect(host="localhost", user="root", passwd="Harmony", db="Harmony_Data_Test")
	c=db_conn.cursor()
	for i in list_to_insert:
		try:
			room = str(i[1])
			occupied = int(i[3])
			occupancy = int(i[4])
			time = int(i[6])
			c.execute("INSERT INTO survey (room_id, occupied, occupancy, timestamp) VALUES (%s, %s, %s, %s)", (room, occupied, occupancy, time))
		except:
			print i
	db_conn.commit()
        return True

def rooms_to_database():
    df = pd.read_csv("./data/Cleaned_Data/room_info.csv", engine="python")
    db_conn = MySQLdb.connect(host="localhost", user="root", passwd="Harmony", db="Harmony_Data_Test")
    c = db_conn.cursor()
    for i in range(df.shape[0]):
        c.execute("INSERT INTO room(room_id, capacity, type, building) VALUES (%s, %s, %s, 'Computer Science')", (df.iloc[i][0], int(df.iloc[i][1]), df.iloc[i][2]))
    db_conn.commit()
    return True

def db_write_timetable(csv):

    # Load csv into dataframe
    df = pd.read_csv(csv, engine="python")
    
    #Get rid of NaN values from the module column
    df1 = df.where((pd.notnull(df)), 0)

    # Convert every pandas row to a tuple, ignoring the index
    # Store all tuples in a list
    list_to_insert = [tuple(x) for x in df1.ix[:,1:].to_records(index=False)]

    # Connect to database and establish cursor
    db_conn = MySQLdb.connect(host='localhost', user='root', passwd='Harmony', db='Harmony_Data_Test')
    c = db_conn.cursor()

    for i in list_to_insert:
	try:
		room = str(i[0])
		time = int(i[1])
		module = str(i[2])
		c.execute("INSERT INTO class(room_id, timestamp, code) VALUES (%s, %s, %s)", (room, time, module))
		db_conn.commit()
	except:
		print i,"Failed"
		
    return True

def db_write_module(csv):

    # Load csv into dataframe
    df = pd.read_csv(csv, engine="python")
    
    # Convert every pandas row to a tuple, ignoring the index
    # Store all tuples in a list
    list_to_insert = [tuple(x) for x in df.ix[:,1:].to_records(index=False)]

    # Connect to database and establish cursor
    db_conn = MySQLdb.connect(host='localhost', user='root', passwd='Harmony', db='Harmony_Data_Test')
    c = db_conn.cursor()
    
    for i in list_to_insert:
        students = int(i[0])
        code = i[1]
        c.execute("INSERT INTO module(code, total_students) VALUES (%s, %s)", (code, students))
    db_conn.commit()
    c.execute("INSERT INTO module(code, total_students) VALUES ('not available', 0)")
    db_conn.commit()
    return True 

if __name__ == "__main__":
    print "Inserting data into database..."
    rooms_to_database()
    db_write_wifi("./data/Cleaned_Data/Cleaned_Wifi_Data.csv")
    insert_ground_data()
    db_write_module("./data/Cleaned_Data/modules.csv")
    db_write_timetable("./data/Cleaned_Data/Cleaned_Timetable_Data.csv")
    print "Data inserted successfully."

