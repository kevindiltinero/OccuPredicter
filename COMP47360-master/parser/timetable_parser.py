import pandas as pd
from numpy.core.numeric import nan, NaN
from datetime import datetime
from time import mktime
import MySQLdb
import sys
import os
#sys.path.insert(0, 'C:/Users/User1/git/comp47360-research-practicum')

# Functions 1-4 extract information from timetable CSV files
def sheet1():
    '''Returns a dataframe of module codes from timetable sheet 1.'''
    
    # Verify that the timetable file exists
    if not os.path.isfile("./data/raw_timetable/timetable_sh1.csv"):
        raise IOError("File './data/raw_timetable/timetable_sh1.csv not found.")
        sys.exit(0)

    # Read in CSV file to a pandas dataframe
    df = pd.read_csv("./data/raw_timetable/timetable_sh1.csv", engine="python")
    
    #Drop unnecessary columns
    cols = [0,2,4,6,8,10,11,12,14,16,18,20,22]
    df.drop(df.columns[cols],axis=1,inplace=True)
    
    # Drop unnecessary rows.
    df.drop(df.index[[0, 10,11,12,13,14,15]], inplace=True)
    
    #Rename columns for simplicity
    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    
    #Insert codes for 2 hour classes
    df['a'][9] = df['a'][8]
    df['b'][7] = df['b'][6]
    df['b'][9] = df['b'][8]
    df['c'][9] = df['c'][8]
    df['d'][8] = df['d'][7]
    df['e'][4] = df['e'][3]
    df['f'][9] = df['f'][8]
    df['g'][7] = df['g'][6]
    df['g'][9] = df['g'][8]
    df['h'][9] = df['h'][8]
    df['i'][8] = df['i'][7]
    df['j'][4] = df['j'][3]
    
    #Remove words "Practical" and "Lecture"
    df['c'][4] = df['c'][4][0:9]
    df['c'][5] = df['c'][4][0:9]
    df['h'][4] = df['h'][4][0:9]
    df['h'][5] = df['h'][4][0:9]
    
    #Stack columns
    frames = [df['a'], df['b'], df['c'], df['d'], df['e'], df['f'], df['g'], df['h'], df['i'], df['j']]
    df = pd.concat(frames)
    
    #Rename columns
    df = df.reset_index(drop=True)
    
    return df

def sheet2():
    '''Returns a dataframe of module codes from timetable sheet 2.'''
    
    # Verify that the timetable file exists
    if not os.path.isfile("./data/raw_timetable/timetable_sh2.csv"):
        raise IOError("File './data/raw_timetable/timetable_sh2.csv not found.")
        sys.exit(0)

    # Read in CSV file to a pandas dataframe
    df = pd.read_csv("./data/raw_timetable/timetable_sh2.csv", engine="python")
    
    #Drop unnecessary columns
    cols = [0,2,4,6,8,10,11,12,14,16,18,20,22]
    df.drop(df.columns[cols],axis=1,inplace=True)
    
    # Drop unnecessary rows.
    df.drop(df.index[[0, 10,11,12,13,14,15]], inplace=True)
    
    #Rename columns for simplicity
    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    
    #Insert codes for 2 hour classes
    df['a'][2] = df['a'][1]
    df['a'][4] = df['a'][3]
    df['a'][7] = df['a'][6]
    df['a'][9] = df['a'][8]
    df['c'][3] = df['c'][2]
    df['c'][5] = df['c'][4]
    df['c'][7] = df['c'][6]
    df['d'][9] = df['d'][8]
    df['e'][2] = df['e'][1]
    df['e'][4] = df['e'][3]
    df['e'][7] = df['e'][6]
    df['f'][2] = df['f'][1]
    df['f'][4] = df['f'][3]
    df['f'][7] = df['f'][6]
    df['f'][9] = df['f'][8]
    df['h'][3] = df['h'][2]
    df['h'][5] = df['h'][4]
    df['h'][7] = df['h'][6]
    df['i'][9] = df['i'][8]
    df['j'][2] = df['j'][1]
    df['j'][4] = df['j'][3]
    df['j'][7] = df['j'][6]
    
    #Remove words "Practical" and "Lecture". 
    df['c'][1] = df['c'][1][0:9]
    df['c'][2] = df['c'][2][0:9]
    df['c'][3] = df['c'][3][0:9]
    df['h'][1] = df['h'][1][0:9]
    df['h'][2] = df['h'][2][0:9]
    df['h'][3] = df['h'][3][0:9]
    
    #Change "Career opportunities talks" to "careers"
    df.replace({'Career opportunities talks': 'careers'}, regex=True, inplace=True)
    
    #Stack columns
    frames = [df['a'], df['b'], df['c'], df['d'], df['e'], df['f'], df['g'], df['h'], df['i'], df['j']]
    df = pd.concat(frames)
    df = df.reset_index(drop=True)
    
    return df

def sheet3():
    '''Returns a dataframe of module codes from timetable sheet 3.'''
    
    # Verify that the timetable file exists
    if not os.path.isfile("./data/raw_timetable/timetable_sh3.csv"):
        raise IOError("File './data/raw_timetable/timetable_sh3.csv not found.")
        sys.exit(0)

    # Read in CSV file to a pandas dataframe
    df = pd.read_csv("./data/raw_timetable/timetable_sh3.csv", engine="python")
    
    #Drop unnecessary columns
    cols = [0,2,4,6,8,10,11,12,14,16,18,20,22]
    df.drop(df.columns[cols],axis=1,inplace=True)
    
    # Drop unnecessary rows.
    df.drop(df.index[[0, 10,11,12,13,14,15]], inplace=True)
    
    #Rename columns for simplicity
    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    
    #Insert codes for 2 hour classes
    df['a'][3] = df['a'][2]
    
    #Remove long string from cell a5. 
    df['a'][5] = NaN
    
    #Stack columns
    frames = [df['a'], df['b'], df['c'], df['d'], df['e'], df['f'], df['g'], df['h'], df['i'], df['j']]
    df = pd.concat(frames)
    df = df.reset_index(drop=True)
    
    return df

def sheet4():
    '''Returns a dataframe of total_students, datetime
    and room_id from timetable sheet 4.'''
    
    # Verify that the timetable file exists
    if not os.path.isfile("./data/raw_timetable/timetable_sh4.csv"):
        raise IOError("File './data/raw_timetable/timetable_sh4.csv not found.")
        sys.exit(0)

    # Read in CSV file to a pandas dataframe
    df = pd.read_csv("./data/raw_timetable/timetable_sh4.csv", engine="python")
    
    # Drop the empty column.
    df = df.drop('Unnamed: 4', 1)
    
    # Drop rows with no data.
    df = df[pd.notnull(df['Week 1'])]
    
    #Rename columns
    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    #Split the data frame vertically in two.
    df1 = df[['a', 'b', 'c', 'd']]
    df2 = df[['e', 'f', 'g', 'h']]
    
    #Rename the columns in the second dataframe to match the names in the first dataframe.
    df2.columns = ['a', 'b', 'c', 'd']
    
    #Concatenate the two dataframes.
    frames = [df1, df2]
    result = pd.concat(frames)
    result = result.reset_index(drop=True)
    
    # Create a new column datetime 
    result.a[result.a=='9:00 - 10:00'] = '09:00 - 10.00'
    result['datetime'] = result['a'].str[0:5] + ':00'
    
    # Add date for week 1 in yyyy/mm/dd format
    result['datetime'][1:10] = '2015/11/02 ' + result['datetime'][1:10]
    result['datetime'][11:20] = '2015/11/03 ' + result['datetime'][11:20]
    result['datetime'][21:30] = '2015/11/04 ' + result['datetime'][21:30]
    result['datetime'][31:40] = '2015/11/05 ' + result['datetime'][31:40]
    result['datetime'][41:50] = '2015/11/06 ' + result['datetime'][41:50]
    
    # Add date for week 2 in yyyy/mm/dd format
    result['datetime'][51:60] = '2015/11/09 ' + result['datetime'][51:60]
    result['datetime'][61:70] = '2015/11/10 ' + result['datetime'][61:70]
    result['datetime'][71:80] = '2015/11/11 ' + result['datetime'][71:80]
    result['datetime'][81:90] = '2015/11/12 ' + result['datetime'][81:90]
    result['datetime'][91:] = '2015/11/13 ' + result['datetime'][91:]
    
    # Drop the old time column
    result = result.drop('a', 1)
    
    # Create a new dataframe for B002
    b002 = result.copy(deep=True)
    
    b002['room_id'] = 'B002'
    
    # Drop columns c and d
    b002.drop(result.columns[[1, 2]], axis=1, inplace=True)
    
    #Drop unnecessary rows
    b002.drop(result.index[[0, 10, 20, 30, 40, 50, 60, 70, 80, 90]], inplace=True)
    
    #Rename column b
    b002.rename(columns={'b': 'total_students'}, inplace=True)
    
    # Create a new dataframe for B003
    b003 = result.copy(deep=True)
    
    # Create a new column for room_id
    b003['room_id'] = 'B003'
    
    # Drop columns b and d
    b003.drop(result.columns[[0, 2]], axis=1, inplace=True)
    
    #Drop unnecessary rows
    b003.drop(result.index[[0, 10, 20, 30, 40, 50, 60, 70, 80, 90]], inplace=True)
    
    #Rename column c
    b003.rename(columns={'c': 'total_students'}, inplace=True)
    
    # Create a new dataframe for B004
    b004 = result.copy(deep=True)
    
    b004['room_id'] = 'B004'
    
    # Drop columns b and c
    b004.drop(result.columns[[0, 1]], axis=1, inplace=True)
    
    #Drop unnecessary rows
    b004.drop(result.index[[0, 10, 20, 30, 40, 50, 60, 70, 80, 90]], inplace=True)
    
    #Rename column d
    b004.rename(columns={'d': 'total_students'}, inplace=True)
    
    #Concatenate the three dataframes.
    frames = [b002, b003, b004]
    table = pd.concat(frames)
    table = table.reset_index(drop=True)
    
    return table


# MAIN FUNCTION
def main():
    '''This code cleans all the timetable data from the timetable csv file and creates a new
    csv file ready for importing into a mysql database'''
    
    print "Extracting Timetable Data..."
    #Get total_students, datetime and all room_id from sheet 4
    df = sheet4()
    
    #Convert datetime column to unix format
    df = unix(df)
    
    #Get a dataframe of all module codes for all rooms
    modules = get_modules()
 
    #Join module codes to existing dataframe
    df['code'] = modules
    
    df.columns = ['students', 'room_id', 'timestamp', 'code']
    
    # Generate a new dataframe for any rows that have more than one module code.
    pairs = separate_pairs(df)
    
    # Concatenate this new dataframe with our main dataframe.
    frames = [df, pairs]
    csv = pd.concat(frames)
    csv = csv.reset_index(drop=True)
    
    # Drop all rows for careers classes
    csv = csv[pd.notnull(csv['students'])]

    # Save the dataframe to csv to allow creation of unique module codes
    csv.to_csv('./data/Cleaned_Data/codes.csv', encoding='utf-8')
    
    # Drop the students columns
    csv = csv.drop('students', 1)
    
    # Set the max number of rows to be printed so we can see the full dataframe when it prints
    pd.set_option('display.max_rows', 300)

    
    # Get rid of NaN values from the module column
    df = csv.where((pd.notnull(csv)), 'not available')
    
    # Save to CSV
    df.to_csv('./data/Cleaned_Data/Cleaned_Timetable_Data.csv')   
    print "Timetable Data successfully extracted."
     

def unix(table):
    '''Converts dates to unix format'''
    timestamps = []
    
    #Convert year, month, day, hour, minute and second for each date to integers
    for i in range(0, table.shape[0]):
        year = table.iloc[i][1][0:4]
        month = table.iloc[i][1][5:7].lstrip("0")
        day = table.iloc[i][1][8:10].lstrip("0")
        hour = table.iloc[i][1][11:13].lstrip("0")
        minute = table.iloc[i][1][14:16]
        if minute == '00': minute = 0
        second = table.iloc[i][1][17:19]
        if second == '00': second = 0
    
        # Create a datetime object with this data
        formatted_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        
        # Convert it to UNIX timestamp and insert into list
        unix_time = int(mktime(formatted_time.timetuple()))
        timestamps.append(unix_time)
    
    #Create new column from list of timestamps
    table['timestamp'] = timestamps
    
    # Drop the old time column
    table = table.drop('datetime', 1)
    return table

def get_modules():
    '''Get module codes from timetable csv sheets 1, 2 and 3.
    Returns a dataframe.'''
    
    #Create a dataframe of modules for each sheet.
    s1 = sheet1()
    s2 = sheet2()
    s3 = sheet3()
    
    #Concatenate the three dataframes.
    frames = [s1, s2, s3]
    modules = pd.concat(frames)
    modules = modules.reset_index(drop=True)
    
    return modules

def separate_pairs(result):
    '''There are six rows with two modules in the code column. 
    Insert a row for each of these modules. Return a dataframe'''
    
    #Remove pandas warnings that we are copying dataframes
    pd.options.mode.chained_assignment = None  # default='warn'
    
    #First row
    # Take the number of students from the comments in the csv(excel) file
    num1 = 19
    num2 = 60
    
    #Copy the row to a new dataframe and add the correct no. of students and module code number.
    pair1 = result.iloc[24]
    pair1['students'] = num1
    mod1 = result['code'][24][12:]
    pair1['code'] = mod1
    
    #Now add correct no. of students and module code number to the row in main dataframe.
    result['students'][24] = num2 # This value for the number of students is taken from a comment in the csv(excel) file
    mod2 = result['code'][24][0:9]
    result['code'][24] = mod2
    
    #Second row has same module codes as row 1 so we can re-use num1 and num2 as well as mod1 and mod2...
    #Second row
    pair2 = result.iloc[69]
    pair2['students'] = num1
    pair2['code'] = mod1
    
    #Now add correct no. of students and module code number to the row in main dataframe.
    result['students'][69] = num2 # This value for the number of students is taken from a comment in the csv(excel) file
    result['code'][69] = mod2
    
    #Third row
    # These two values for the number of students are taken from a comment in the csv(excel) file
    num1 = 108
    num2 = 35
    
    pair3 = result.iloc[189]
    pair3['students'] = num1
    mod1 = result['code'][189][12:]
    pair3['code'] = mod1
    
    #Now add correct no. of students and module code number to the row in main dataframe.
    result['students'][189] = num2 
    mod2 = result['code'][189][0:9]
    result['code'][189] = mod2
    
    #Fourth, fifth and sixth rows have same module codes as row 3 so we can re-use num1 and num2 as well as mod1 and mod2...
    #Fourth row
    pair4 = result.iloc[207]
    pair4['students'] = num1
    pair4['code'] = mod1
    result['students'][207] = num2 
    result['code'][207] = mod2

    #Fifth row
    pair5 = result.iloc[234]
    pair5['students'] = num1
    pair5['code'] = mod1
    result['students'][234] = num2 
    result['code'][234] = mod2
    
    #Sixth row
    pair6 = result.iloc[252]
    pair6['students'] = num1
    pair6['code'] = mod1
    result['students'][252] = num2 
    result['code'][252] = mod2
    
    #Concatenate the extracted modules into one dataframe
    frames = [pair1, pair2, pair3, pair4, pair5, pair6]
    df = pd.DataFrame(frames)
    df = df.reset_index(drop=True)
    
    return df

if __name__ == '__main__':
    main()
