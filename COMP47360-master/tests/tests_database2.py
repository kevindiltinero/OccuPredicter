# -*- coding: utf-8 -*-

import pandas as pd
import unittest



def room_type(cur, room_name):
    cur.execute("SELECT type FROM room WHERE room_id = '{0}'".format(str(room_name)))
    results = cur.fetchall()
    if not results:
        return None
    if not results[0]:
        return None
    return cur.fetchall()[0][0]  #fetching data from database

import MySQLdb

class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.db = MySQLdb.connect(host="localhost",    #localhost
                     user="root",         #username
                     passwd="Harmony",   #password
                     db="harmony_data_test")      #database name


    def test_room(self):
        #Check the correct room type is returned 
        cur = self.db.cursor()
        result_type = room_type(cur, "B106")
        self.assertTrue(result_type == "A.L.E.")


    


    def tearDown(self):
        self.db.close()


if __name__ == '__main__':
    unittest.main()
