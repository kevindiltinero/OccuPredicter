##################################################################################################
#########################################  GROUND TRUTH  #########################################
##################################################################################################
from datetime import datetime
from time import mktime
import pandas as pd
import csv
import re
import os
import sys

# CLEAN THE GROUND FILE
def ground_clean():

    # Check if the necessary ground truth raw data file is found
    # Print a success message if it is found
    if os.path.isfile("data/raw_ground/CSI Occupancy Report.xlsx"):
        print "Extracting Ground Truth Data..."
        os.rename("data/raw_ground/CSI Occupancy Report.xlsx", "data/raw_ground/CSIOccupancyReport.xlsx")

    elif os.path.isfile("data/raw_ground/CSIOccupancyReport.xlsx"):
        print "Extracting Ground Truth Data..."
        
    # Otherwise, raise an Exception with description message
    # Cease running the script
    else:
        raise IOError("Ground Truth file not found.  Please check that it is named correctly, and located in './data/raw_ground/'.")
        sys.exit(0)

    # Select correct sheet from excel file and drop empty columns
    df = pd.read_excel("./data/raw_ground/CSIOccupancyReport.xlsx", sheetname="CSI")

    df.drop([df.columns[1], df.columns[3], df.columns[9]], axis=1, inplace=True)
    
    # Save to separate CSV file
    df.to_csv("./data/raw_ground/Occupancy.csv", index=False, header=False)
    df.set_index(df[0], inplace=True)

    # Standard python opening the file.
    with open('./data/raw_ground/Occupancy.csv', 'r') as file:

        # Create a reader object, feed in the csv file as a parameter to reader, turns lines into lists
        reader = csv.reader(file)

        # Reader not subscribable so take lists and pop them into a nested list for more control.
        whole_csv = list(reader) 

        # TABLES: Use regular expressions to pull out the appropriate lines based on the time stamp pattern
        # Create separate lists for % Occupancy and Over 3 records
        occ_lines = []
        over3_lines = []
        over3 = True
        count = 0

        for line in whole_csv:
            #Regex; check if the first element of each line begins with the time format
            if re.match(r'(\d{1,2}\.\d{2}-\d{2}\.\d{2})', line[0], flags=0):
                if over3:
                    over3_lines.append(line)
                    count += 1
                    if count == 8:
                        count = 0
                        over3 = False
                else:
                    occ_lines.append(line)
                    count += 1
                    if count == 8:
                        count = 0
                        over3 = True

        # DATES: Use this to pull the dates and save them in a separate list
        date_lines = []
        for line in whole_csv:
            #Regex; check if the first element of each line begins with the date format
            if re.match(r'(\d[nd].*|\d[rd].*|\d[th].*|\d{2}[th].*)', line[0], flags=0):
                if line[0] not in date_lines:
                    date_lines.append(line[0])

        # ROOMS: Information on the rooms
        room_lines = ['B004', 'B002', 'B003', 'B106', 'B108', 'B109']
        capacity_lines = [160, 90, 90, 90, 40, 90]
        classroom_type = ["Lecture Theatre", "Classroom", "Classroom", "A.L.E.", "Seminar", "Seminar"]

        # List to store entries
        ground_lines = []

        # Every 8 entries will change over to a new date
        # Append the appropriate information to the list
        date_counter = 0
        other_counter=0
        day_list = {
                "1st":1,
                "2nd":2,
                "3rd":3,
                "4th":4,
                "5th":5,
                "6th":6,
                "7th":7,
                "8th":8,
                "9th":9,
                "10th":10,
                "11th":11,
                "12th":12,
                "13th":13,
                "14th":14,
                "15th":15,
                "16th":16,
                "17th":17,
                "18th":18,
                "19th":19,
                "20th":20,
                "21st":21,
                "22nd":22,
                "23rd":23,
                "24th":24,
                "25th":25,
                "26th":26,
                "27th":27,
                "28th":28,
                "29th":29,
                "30th":30,
                "31st":31
                }
        for i in range(len(over3_lines)):
            for j in range(len(room_lines)):
                year = int(date_lines[date_counter].split()[-1])
                month = 11
                day = day_list[date_lines[date_counter].split()[0]]
                hour = int(over3_lines[i][0].split(".")[0])
                dt = datetime(year=year,month=month,day=day,hour=hour)
                unixtime = mktime(dt.timetuple())
                
                ground_lines.append([over3_lines[i][0], room_lines[j], capacity_lines[j], over3_lines[i][j+1], int(float(occ_lines[i][j+1])*100), date_lines[date_counter], int(unixtime), classroom_type[j]])
            other_counter+=1
            if other_counter == 8:
                date_counter+=1
                other_counter = 0

        # Write final information to a CSV file
        output_file = open("./data/Cleaned_Data/Cleaned_Ground_Data.csv", "wb")
        wr = csv.writer(output_file, dialect="excel")
        wr.writerows(ground_lines)
        print "Ground Truth Data successfully extracted."
        
if __name__ == "__main__":
    ground_clean()
