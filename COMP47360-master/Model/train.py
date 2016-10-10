################################################################################
# All of this script is available in a clearer format in the iPython Notebook ##
# found in the 'docs' folder.                                                 ##
################################################################################

# IMPORT ALL THE REQUIRED PACKAGES.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import linear_model
from sklearn import svm
from sklearn import preprocessing
from sklearn import tree
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals.six import StringIO
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import GridSearchCV
import itertools
import warnings
warnings.filterwarnings('ignore')
import pickle
import os
import re
import calendar
from datetime import datetime
import MySQLdb


format_timestamp = lambda x:datetime.fromtimestamp(int(x))
format_weekday = lambda x:calendar.day_name[x]

def split_timestamp(df):
    # Iterate through all rows and split column timestamp for three different values
    weekdays, dates, times, months, years = [], [], [], [], []
    for timestamp in df["timestamp"]:
        weekdays.append(timestamp.weekday())
        dates.append(timestamp.strftime("%Y-%m-%d"))
        times.append(timestamp.strftime("%H:%M:%S"))
        months.append(timestamp.strftime("%B"))
        years.append(int(timestamp.strftime("%Y")))
    return weekdays, dates, times, months, years

def format_timerange(x):
    # Change column time to format in range 9:00 - 10:00, 10:00-11:00 etc
    hour = int(x.split(':')[0])  # split time,choose first element (hour) and change to integer
    return "{}:00-{}:00".format(str(hour).zfill(2), str(hour+1).zfill(2))  # zfill adds extra zero to the hour

# Function as an argument takes input dataframe and returns dataframe with added extra columns Weekday,Date, Time
def prepare_timestamp(df):
    # Convert the unix timestamp into regular datetime

    df["timestamp"] = df["timestamp"].map(format_timestamp)
    
    # Split column timestamp for three different values and assign columns name
    weekdays, dates, times, months, years = split_timestamp(df)

    df['Weekday'] = weekdays
    df['Date'] = dates
    df['Time'] = times
    df['Month'] = months
    df['Year'] = years
    
    df['Weekday'] = df['Weekday'].map(format_weekday)#Mapping weekday number to name (Monday, Tuesday, Wednesday, Thursday, Friday)
    
    # Remove Saturday and Sunday from dataframe
    df = df[(df['Weekday'] != 'Saturday') & (df['Weekday'] != 'Sunday')]
    
   
    # Set index on timestamp to choose time between 09:00 - 17:00
    df = df.set_index('timestamp')
    df = df.between_time('09:00','17:00')
    
    # Change column time to format in range 9:00 - 10:00, 10:00-11:00 etc
    df['Time'] = df['Time'].map(format_timerange) #Map iterates over each element of a series. 
    
    return df


# 1. READING FROM DATABASE
#===============================================================================
print "Beginning analytical model setup."
print "Opening database connection."
# Connect to the database
db = MySQLdb.connect(host="localhost",    # localhost
                     user="root",         # username
                     passwd="Harmony",   # password
                     db="Harmony_Data_Test")      # name of the data base

print "Reading data from database."
# Use pandas "read_sql" to put information from database into dataframes
logs_df = pd.read_sql(sql="select room_id, timestamp, authenticated, associated from wifi ", con = db)
ground_df = pd.read_sql(sql="select r.capacity, r.type, r.room_id, s.occupied, s.occupancy, s.timestamp from survey as s join room as r on s.room_id = r.room_id", con = db)
timetable_df = pd.read_sql(sql="select c.timestamp, c.room_id, c.code,m.total_students from class as c join module as m on c.code = m.code ", con = db)

print "Database read complete. Closing connection."
print "Formatting data."
# Close database connection
db.close() 

# Split column timestamp for three different values
logs_df = prepare_timestamp(logs_df)
ground_df = prepare_timestamp(ground_df)
timetable_df = prepare_timestamp(timetable_df)


# 2. SELECTING THE MAX ASSOCIATED VALUE
#===============================================================================
hours = ["{}:00".format(hour) for hour in range(9, 18)]  #we get list: ['9:00', '10:00', ..., '16:00']

output_data = pd.DataFrame(columns=logs_df.columns)  #creating empty output table based on input table

for room in logs_df['room_id'].unique():  # for each room
    room_data = logs_df[logs_df['room_id'] == room]  #select data only from the room
    for date in room_data['Date'].unique():  # for each date
        date_logs_df = room_data[room_data['Date'] == date]  #selec data only form the date
        
        for index in range(len(hours)-1):  # for each range of hour
            time_data = date_logs_df.between_time(hours[index], hours[index+1])  #select only data from a given time period
            if time_data["associated"].count(): #checking whether a given period of time, there is at least one row 
                max_value = time_data["associated"].max()  # choosing the max Assoc from selected data
                max_time_data = time_data[time_data["associated"] == max_value].iloc[0]  #selecting a first element of a maximum value of a column
                output_data = output_data.append(max_time_data)  #append a row to the output data


# 3. MERGING INTO SINGLE DATAFRAME
#===============================================================================
print "Merging data to form Analytics Base Table."
result = output_data.merge(ground_df,on=['room_id','Weekday','Date','Time','Month','Year']).merge(timetable_df,on=['room_id','Weekday','Date','Time','Month','Year'])

# When no wifi data available
result2 = pd.merge(ground_df, timetable_df, on=['room_id','Weekday','Date','Time', 'Month', 'Year'])

# When no wifi or module data available
result3 = ground_df[:]

# Drop the date column, as it is represented by 3 individual columns now
result = result.drop(["Date"], axis=1)
result2 = result2.drop(["Date"], axis=1)
result3 = result3.drop(["Date"], axis=1)

# Name the columns
result.columns =["Room", "Authenticated", "Associated", "Day", "Time", "Month", "Year", "Capacity", "Type", "Over3", "TARGET", "Module","Registered"]
result2.columns = ["Capacity", "Type", "Room", "Over3", "TARGET", "Day", "Time", "Month", "Year", "Module", "Registered"]
result3.columns = ["Capacity", "Type", "Room", "Over3", "TARGET", "Day", "Time", "Month", "Year"]

# Re-order the columns as desired
new_cols = ["Time", "Day", "Month", "Year", "Module", "Room", "Type", "Capacity", "Registered", "Authenticated", "Associated", "Over3", "TARGET"]
result = result[new_cols]

# Output to CSV file
result.to_csv("./docs/TableABT.csv")
print "Analytics Base Table to 'docs' directory as 'TableABT.csv'."

# 4. ENCODING CATEGORICAL FEATURES
#===============================================================================

# Use dictionaries to allow for easy conversion between days/months and fixed integers
day_dict = {
    "Monday":0,
    "Tuesday":1,
    "Wednesday":2,
    "Thursday":3,
    "Friday":4,
    "Saturday":5,
    "Sunday":6
}

month_dict = {
    "January":1,
    "February":2,
    "March":3,
    "April":4,
    "May":5,
    "June":6,
    "July":7,
    "August":8,
    "September":9,
    "October":10,
    "November":11,
    "December":12
}

# List of what the module codes map to
module_codes = {'COMP30190': 15, 'COMP10280': 2, 'COMP47300': 27, 'STAT40150': 32, 
                'COMP40370': 21, 'COMP20020': 4, 'COMP30250': 18, 'COMP30120': 13,
                'COMP41690': 25, 'not available': 33, 'SCI30060': 31, 'COMP30060': 9,
                'COMP40660': 22, 'MATH10200': 30, 'COMP30080': 11, 'COMP30520': 20,
                'ENVB30110': 28, 'MATH10130': 29, 'COMP20010': 3, 'COMP20130': 7,
                'COMP30110': 12, 'COMP20110': 6, 'COMP30070': 10, 'COMP20070': 5,
                'COMP30240': 17, 'COMP30010': 8, 'COMP30170': 14, 'COMP30260': 19,
                'COMP41110': 23, 'COMP30220': 16, 'COMP47290': 26, 'COMP10130': 1,
                'COMP10110': 0, 'COMP41450': 24, 'IS40640': 34}
# Room types
type_codes = {'Classroom':0, 'Lecture Theatre':1, 'A.L.E.':2, 'Seminar':3}

# Use the above dictionaries to manually encode days and months to always be the correct integer
day_list = []
month_list = []
module_list = []
type_list = []
for i in range(len(result)):
    month_list.append(month_dict[result.iloc[i]["Month"]])
    day_list.append(day_dict[result.iloc[i]["Day"]])
    module_list.append(module_codes[result.iloc[i]["Module"]])
    type_list.append(type_codes[result.iloc[i]["Type"]])
# Reassign to the dataframe
result.Day = day_list
result.Month = month_list
result.Module = module_list
result.Type = type_list

# Same thing for dataframe without WiFi
day_list2 = []
month_list2 = []
module_list2 = []
type_list2 = []
for i in range(len(result2)):
    month_list2.append(month_dict[result2.iloc[i]["Month"]])
    day_list2.append(day_dict[result2.iloc[i]["Day"]])
    module_list2.append(module_codes[result2.iloc[i]["Module"]])
    type_list2.append(type_codes[result2.iloc[i]["Type"]])
result2.Day = day_list2
result2.Month = month_list2
result2.Module = module_list2
result2.Type = type_list2

# Same thing for dataframe without WiFi and Modules
day_list3 = []
month_list3 = []
type_list3 = []
for i in range(len(result3)):
    month_list3.append(month_dict[result3.iloc[i]["Month"]])
    day_list3.append(day_dict[result3.iloc[i]["Day"]])
    type_list3.append(type_codes[result3.iloc[i]["Type"]])
result3.Day = day_list3
result3.Month = month_list3
result3.Type = type_list3

# Categorical features to encode
column_names = ['Time', 'Room', 'TARGET']

print "Encoding categorical features."
# Succint function for integer representation
lab_enc = preprocessing.LabelEncoder()

# Iteratively encode all the columns for each dataframe
for name in column_names: 
    if name in result.columns:
        result[name] = lab_enc.fit_transform(result[name])
    if name in result2.columns:
        result2[name] = lab_enc.fit_transform(result2[name])
    if name in result3.columns:
        result3[name] = lab_enc.fit_transform(result3[name])

print "Encoded Analytics Base Table saved to 'docs' directory as 'EncodedABT.csv'."
# Output encoded dataframe to csv
result.to_csv("./docs/EncodedABT.csv")

print "Connecting to database."
# Write this data to the database
db = MySQLdb.connect(host="localhost",    # localhost
                     user="root",         # username
                     passwd="Harmony",   # password
                     db="Harmony_Data_Test")      # name of the data base

print "Database connection successful. Writing encoded analytics base table to 'Harmony_Data_Test.abt'"
result.to_sql("abt", db, flavor="mysql", if_exists="replace", index=False)
print "Database write complete. Closing connection"

# Close connection
db.close()

# Declare descriptive columns for the case where all data is available
all_descriptive = ['Day', 'Time', 
                   'Module', 'Room', 'Capacity', 
                   'Type', 'Registered', 
                   'Authenticated', 'Associated', 'Year', 'Month']
X = result[all_descriptive]
Y = result['TARGET']   

# Case 2
all_descriptive2 = ['Day', 'Time', 
                   'Module', 'Room', 'Capacity', 
                   'Type', 'Registered', 
                   'Year', 'Month']
X2 = result2[all_descriptive2]
Y2 = result2['TARGET']

# Case 3
all_descriptive3 = ['Day', 'Time', 'Room', 'Capacity', 
                   'Type', 'Year', 'Month']
X3 = result3[all_descriptive3]
Y3 = result3['TARGET']

# Variance Threshold
sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
features = sel.fit_transform(X)
features[0]

# Case 2
sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
features2 = sel.fit_transform(X2)
features2[0]

# Case 3
sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
features3 = sel.fit_transform(X3)
features3[0]

# Univariate feature selection
X_new = SelectKBest(chi2, k=11).fit_transform(X, Y)
df = pd.DataFrame(X_new, columns=['Day', 'Month', 'Year', 'Time', 'Module', 'Room', 'Capacity', 'Type', 'Registered', 'Authenticated', 'Associated'])
columns = df.columns

# Case 2
X_new2 = SelectKBest(chi2, k=9).fit_transform(X2, Y2)
df2 = pd.DataFrame(X_new2, columns=['Day', 'Month', 'Year', 'Time', 'Module', 'Room', 'Capacity', 'Type', 'Registered'])
columns2 = df2.columns

# Case 3
X_new3 = SelectKBest(chi2, k=7).fit_transform(X3, Y3)
df3 = pd.DataFrame(X_new3, columns=['Day', 'Month', 'Year', 'Time', 'Room', 'Capacity', 'Type'])
columns3 = df3.columns

# 5. RECURSIVE FEATURE ELIMINATION
#===============================================================================
feature_combinations = []
feature_combinations2 = []
feature_combinations3 = []

# Case 1
for L in range(0, len(columns)+1):
    for subset in itertools.combinations(columns, L):
        feature_combinations.append(list(subset))
# Case 2
for L in range(0, len(columns)+1):
    for subset in itertools.combinations(columns2, L):
        feature_combinations2.append(list(subset))
# Case 3
for L in range(0, len(columns)+1):
    for subset in itertools.combinations(columns3, L):
        feature_combinations3.append(list(subset))   

# Cleanup    
del feature_combinations[0]
del feature_combinations2[0]
del feature_combinations3[0]

# 6. MODEL EVALUATION
#===============================================================================
# DECISION TREE
tree = tree.DecisionTreeClassifier()
# K NEAREST NEIGHBOURS
knn = KNeighborsClassifier()
# LOGISTIC REGRESSION
logreg = linear_model.LogisticRegression()
# LINEAR REGRESSION
linear = linear_model.LinearRegression()

def feature_model_comb(model):
    # CROSS VALIDATION
    # This will keep track of the results of each feature combination used with each model.
    compare_results = []
    compare_results2 = []
    compare_results3 = []

    # This just prints integer signature for each combination
    combination_labels = range(len(feature_combinations))
    combination_labels2 = range(len(feature_combinations2))
    combination_labels3 = range(len(feature_combinations3))
        
    for combination in feature_combinations:
        # PANDAS trick to change columns quickly
        X = df.as_matrix(columns = combination)
        y = result.as_matrix(columns = ['TARGET']).ravel()

        # Use cross validation accuracy for better generalisation    
        # Get the mean of the results 
        # USE THIS LINE FOR CATEGORICAL FEATURES
        compare_results.append(cross_val_score(model, X, y, cv=10, scoring='accuracy').mean())
        
        # USE THIS LINE FOR CONTINUOUS FEATURES        
        # scores = cross_val_score(knn, X, y, cv=10, scoring='mean_squared_error')        
    
    # Exactly the same thing for the lists without wifi data
    for combination in feature_combinations2:
        X = df2.as_matrix(columns = combination)
        y = result2.as_matrix(columns = ['TARGET']).ravel()
        compare_results2.append(cross_val_score(model, X, y, cv=10, scoring='accuracy').mean())
    
    # And same thing again excluding wifi and timetable data
    for combination in feature_combinations3:
        X = df3.as_matrix(columns = combination)
        y = result3.as_matrix(columns = ['TARGET']).ravel()
        compare_results3.append(cross_val_score(model, X, y, cv=10, scoring='accuracy').mean())
        
    # Return all results as well as lists
    return [[combination_labels, combination_labels2, combination_labels3], [compare_results, compare_results2, compare_results3]]

# PLEASE SEE THE iPYTHON NOTEBOOK FOR VISUAL MODEL EVALUATION
# # Tree
# print "Please wait while Decision Tree is evaluated (This may take a few minutes)."
# tree_results = feature_model_comb(tree)
# print "Decision Tree evaluation complete"
# 
# # KNN 
# print "Please wait while KNN is evaluated (This may take a few minutes)."
# knn_results = feature_model_comb(knn)
# print "KNN evaluation complete"
# 
# # Logistic Regression
# print "Please wait while Logisitic Regression is evaluated (This may take a few minutes)."
# logreg_results = feature_model_comb(logreg)
# print "Logisitic Regression evaluation complete"
# 
# 
# # 7. COMPARE MODELS
# #===============================================================================
# # Standard case
# knn_result = max(knn_results[1][0])
# tree_result = max(tree_results[1][0])
# logreg_result = max(logreg_results[1][0])
# 
# models = range(3)
# model_results = [knn_result, tree_result, logreg_result]

# # No wifi data available
# knn_result2 = max(knn_results[1][1])
# tree_result2 = max(tree_results[1][1])
# logreg_result2 = max(logreg_results[1][1])
# 
# models2 = range(3)
# model_results2 = [knn_result2, tree_result2, logreg_result2]
# 
# # No wifi or module data
# knn_result3 = max(knn_results[1][2])
# tree_result3 = max(tree_results[1][2])
# logreg_result3 = max(logreg_results[1][2])
# 
# models3 = range(3)
# model_results3 = [knn_result3, tree_result3, logreg_result3]
# # 8. PARAMETER TUNING
# #===============================================================================
# PARAMETER VALUES
criterion_options = ['gini', 'entropy']
splitter_options = ['best', 'random']
presort_options = [True, False]
max_fea_range_op = list(range(20))
max_depth_op = list(range(1, 30))
min_samples_leaf_op = list(range(1, 4))
k_range = list(range(1, 91))
# GRID
param_grid = dict(criterion=criterion_options, splitter=splitter_options,
                  presort= presort_options, max_depth=max_depth_op, 
                  min_samples_leaf=min_samples_leaf_op)
# Execute the grid
grid = GridSearchCV(tree, param_grid, cv=10, scoring='accuracy')
X = result.as_matrix(columns = ['Day', 'Month', 'Time'])
Y = result.as_matrix(columns = ['TARGET']).ravel()
print "Applying grid fitting for parameter tuning. Please wait..."
grid.fit(X, Y)
print "Grid fitting complete."

# Grid scores
grid_mean_scores = [x.mean_validation_score for x in grid.grid_scores_]
labelling = list(range(len(grid_mean_scores)))

# 9. DEPLOYMENT VIA PICKLE
#===============================================================================
# Create a directory to save the classifiers to
destination = os.path.join('occupancyclassifier', 'pk1objects')
if not os.path.exists(destination):
    os.makedirs(destination)
    
# Train the first classifier and save to pickle file
X = result.as_matrix(columns = ['Module', 'Room', 'Registered', 'Authenticated', 'Associated'])
y = result.as_matrix(columns = ['TARGET']).ravel()
tree.fit(X, y)
pickle.dump(tree, open(os.path.join(destination, 'occupancyclassfier.pk1'), 'wb'), protocol=2)    

# Repeat for model without wifi data
X2 = result2.as_matrix(columns = ['Month', 'Capacity', 'Type', 'Registered'])
y2 = result2.as_matrix(columns = ['TARGET']).ravel()
tree.fit(X2, y2)
pickle.dump(tree, open(os.path.join(destination, 'occupancyclassfier2.pk1'), 'wb'), protocol=2)    

# And again for model without wifi or timetable data
X3 = result3.as_matrix(columns = ['Day', 'Month', 'Capacity', 'Type'])
y3 = result3.as_matrix(columns = ['TARGET']).ravel()
tree.fit(X3, y3)    
pickle.dump(tree, open(os.path.join(destination, 'occupancyclassfier3.pk1'), 'wb'), protocol=2)    

print "Process Completed successfully."
print "3 pickle object files have been created at 'occupancyclassifier/pk1objects/'."
raw_input("Hit any key to continue...")
