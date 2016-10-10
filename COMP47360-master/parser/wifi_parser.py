from datetime import datetime
from time import mktime
import os
import pandas as pd
import MySQLdb

def main():
    
    print "Extracting Wifi Data..."
    # Specify the target file to write to
    target_file="./data/Cleaned_Data/Cleaned_Wifi_Data.csv"

    # Check that a wifi log file does not exist already
    # If it does, delete that and write to a new file
    if os.path.isfile(target_file):
        os.remove(target_file)

    # Select all of the files from the WiFi Log directory
    file_list = os.listdir("./data/raw_wifi/CSI WiFiLogs")

    # If the correct number of files are not found, exit with Exception
    if len(file_list) != 1053:
        raise IOError("Incorrect number of wifi logs found.  Expected 1053 files.  Found "+str(len(file_list))+" files.")
        sys.exit(0)

    # For each file, clean into a proper dataframe, and append that to the target file
    map(lambda x:write_wifi(parse_wifi("./data/raw_wifi/CSI WiFiLogs/"+x), target_file), file_list)
    print "Wifi Data successfully extracted."


def write_wifi(dataframe, path_to_file):
    """Writes the contents of a dataframe to a specific CSV file"""
    exists = os.path.isfile(path_to_file)

    with open(path_to_file, "a") as f:
        dataframe.to_csv(f, header=not(exists))

    return


def parse_wifi(csvfile):
    """Extracts data of interest from WiFi log files

    Returns a pandas dataframe containng this information"""

    # Create names for columns
    col_names = ["Room", "Time", "Assoc", "Auth"]
    # Read in CSV file to a pandas dataframe
    df = pd.read_csv(csvfile, names=col_names, engine="python")

    # Cycle through the first column until the work 'Key'
    # All data of interest is below this, so delete above
    for i in range(0, df.shape[0]-1):
        if df.iloc[i][0] == "Key":
            break
    df_data = df.ix[i+1:]
    del df

    # Dictionary to allow conversion of date abbreviations to numerical form
    month_dictionary = {
        "Jan":1,
        "Feb":2,
        "Mar":3,
        "Apr":4,
        "May":5,
        "Jun":6,
        "Jul":7,
        "Aug":8,
        "Sep":9,
        "Oct":10,
        "Nov":11,
        "Dec":12
    }


    # Cycle through all cells relating to room and time
    for i in range(0, df_data.shape[0]):
        room = df_data.iloc[i][0].split()[-1]
        # Remove punctuation from room name and insert back into dataframe
        room = room.replace("-","")
        df_data.iloc[i][0] = room
        
        # Split up the time column into individual components
        time_properties = df_data.iloc[i][1].split()
        year = time_properties[-1]
        month = month_dictionary[time_properties[1]]
        day = time_properties[2]
        hour = time_properties[3].split(":")[0]
        minute = time_properties[3].split(":")[1]
        second = time_properties[3].split(":")[2]

        # Create a datetime object with this data
        formatted_time = datetime(int(year), month, int(day), int(hour), int(minute), int(second))
        # Convert it to UNIX timestamp and insert back into dataframe
        unix_time = int(mktime(formatted_time.timetuple()))
        df_data.iloc[i][1] = unix_time

    return(df_data)

if __name__ == '__main__':
    main()
