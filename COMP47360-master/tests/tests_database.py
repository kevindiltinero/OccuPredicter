# -*- coding: utf-8 -*-
import pandas as pd
import unittest
from datetime import datetime, time
import calendar
import MySQLdb

class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.db = MySQLdb.connect(host="localhost",    #localhost
                     user="root",         #username
                     passwd="Motylek80",   #password
                     db="harmony_data_test")      #database name


    def test_wifi_columns(self):
        # test correct columns name in wifi table_
        cur = self.db.cursor()  # get a cursor object which is used to manage the context of a fetch operation
        cur.execute("SELECT * FROM wifi")  #query to select all data from wifi table
        fields = map(lambda x:x[0], cur.description)  #fetch all columns name in table wifi

        expected_values = ['record_id', 'room_id', 'timestamp', 'authenticated', 'associated']
        for index, field in enumerate(fields):
            self.assertTrue(field==expected_values[index])



    def test_wifi_room_id(self):
        #check that the correct room number is returned  

        cur = self.db.cursor()  #get a cursor object which is used to manage the context of a fetch operation
        cur.execute("SELECT room_id FROM wifi limit 10")  #query to select room_id from wifi table

        data = [row for row in cur.fetchall()]  #fetch data from database
        for row in data:
            self.assertTrue(row[0] == "B002")


    def test_wifi_authenticated(self):
        #heck the max value authenticated for the room B004
        cur = self.db.cursor()  #get a cursor object which is used to manage the context of a fetch operation
        cur.execute("SELECT authenticated FROM wifi where room_id='B004' order by authenticated desc")  #query to select column authenticated from wifi where room_id B004 order by desc

        data = [row for row in cur.fetchall()]  #fetch data from database
        self.assertTrue(data[0][0] == 230)


    def tearDown(self):
        self.db.close()



if __name__ == '__main__':
    unittest.main()
