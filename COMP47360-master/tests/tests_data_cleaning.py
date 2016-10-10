# -*- coding: utf-8 -*-
import pandas as pd
import unittest
from datetime import datetime, time
import calendar

class TestWifiDataMethods(unittest.TestCase):

    def setUp(self):
        # The initial configuration of the tests, the preparation of relevant data
        self.wifi_data = pd.read_csv("./wifi_data.csv")
        format_timestamp = lambda x:datetime.fromtimestamp(int(x))
        self.wifi_data['Timestamp'] = self.wifi_data['Timestamp'].map(format_timestamp)

        #iterate through all rows and split column timestamp for three different values
        weekdays, dates, times = [], [], []
        for timestamp in self.wifi_data['Timestamp']:
            weekdays.append(timestamp.weekday())
            dates.append(timestamp.strftime("%Y-%m-%d"))
            times.append(timestamp.strftime("%H:%M:%S"))

        #split column timestamp for three different values and assign columns name
        self.wifi_data['Weekday'] = weekdays
        self.wifi_data['Date'] = dates
        self.wifi_data['Time'] = times

        format_weekday = lambda x:calendar.day_name[x]
        self.wifi_data['Weekday'] = self.wifi_data['Weekday'].map(format_weekday)#Mapping weekday number to name (Monday, Tuesday, Wednesday, Thursday, Friday)


    def test_weekday(self):
        # test to check if our dataset has no Saturday and Sunday
        wifi_data = self.wifi_data  #Copying data to a local variable

        errors = 0  #setting the current number of errors at 0
        for row in wifi_data['Weekday']:  # checking whether any raw in dataset is equal to the Saturday or Sunday
            if row == "Saturday":
                errors += 1
            if row == "Sunday":
                errors += 1 

        self.assertFalse(errors == 0)  # #the file is not filtered so the test should fail therefore assert False

        wifi_data = wifi_data[(wifi_data['Weekday'] != 'Saturday') & (wifi_data['Weekday'] != 'Sunday')]  #filtering data

        errors = 0
        for row in wifi_data['Weekday']:  # checking whether any raw in dataset is equal to the Saturday or Sunday

            if row == "Saturday":
                errors += 1
            if row == "Sunday":
                errors += 1

        self.assertTrue(errors == 0)


    def test_timestamp(self):
        # test to check correct hours
        wifi_data = self.wifi_data  # Copying data to a local variable


        errors = 0  # setting the current number of errors at 0
        for row in wifi_data['Timestamp']:  #checking whether any raw in dataset is not in range between 09:00 -17:00
            if row.time() < time(9, 00):
                errors += 1
            if row.time() > time(17, 00):
                errors += 1

        self.assertFalse(errors == 0)  #the file is not filtered so the test should fail therefore assert False

        wifi_data = wifi_data.set_index('Timestamp')
        wifi_data = wifi_data.between_time('09:00','17:00')

        errors = 0  #setting the current number of errors at 0
        for row in wifi_data.index:  # checking whether any raw in dataset is not in range between 09:00 -17:00
            if row.time() < time(9, 00):
                errors += 1
            if row.time() > time(17, 00):
                errors += 1

        self.assertTrue(errors == 0)


    def test_bestvalue(self):
        # test to check the max value from the dataset choosen in each hour between 09:00-17:00
        wifi_data = self.wifi_data.head(50)  # Copying data to a local variable, checking just subset of 50 instances
        wifi_data = wifi_data.set_index('Timestamp')
        wifi_data = wifi_data.between_time('09:00','17:00')

        hours = ["{}:00".format(hour) for hour in range(9, 18)]  #get a list: ['9:00', '10:00', ..., '16:00']
        output_data = pd.DataFrame(columns=wifi_data.columns)  # to create an empty table based on the output of the input table

        for room in wifi_data['Room'].unique():  # for each room
            room_data = wifi_data[wifi_data['Room'] == room]  # select data only from the room
            for date in room_data['Date'].unique():  # for each day 
                date_wifi_data = room_data[room_data['Date'] == date]  # select data only from the date

                for index in range(len(hours)-1):  # dla każdego przedziału godzin
                    time_data = date_wifi_data.between_time(hours[index], hours[index+1])  # wybranie danych tylko z danego przedziału czasu
                    if time_data["Assoc"].count():  # sprawdzenie czy dla danego przedziału czasu istnieje chociaż jeden wiersz
                        max_value = time_data["Assoc"].max()  # wybranie maksymalnej wartości dla klumny Associated z przefiltrowanych danych
                        max_time_data = time_data[time_data["Assoc"] == max_value].iloc[0]  # wybranie pierwszego elementu o maksymalnej wartości kolumny
                        output_data = output_data.append(max_time_data)  # dodanie wiersza do wyjściowej tabeli

        expected_values = [9, 17, 19, 20, 16, 20, 16, 20, 21, 11, 21, 32, 36, 31, 29, 51, 58, 41, 3, 16] # poprawne wartości
        for index, row in enumerate(wifi_data["Assoc"]):

            self.assertTrue(row == expected_values[index])  # sprawdzenie czy wartość wyjściowa algorytmu jest równa wartości oczekiwanej



    


   




if __name__ == '__main__':
    unittest.main()
