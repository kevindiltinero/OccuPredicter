# -*- coding: utf-8 -*-

import pandas as pd
import unittest


def data_cleaning(x):
    return x[x['code'].notnull()]



class TestWifiDataMethods(unittest.TestCase):

    def setUp(self):
        self.timetable = pd.read_csv("Timetable.csv")

    def test_null(self):
        #test check if null values are not in table
        cleaned_timestamp = data_cleaning(self.timetable)

        for x in cleaned_timestamp.isnull().sum() == 0:
            self.assertTrue(x)


    def test_rows(self):
        #test check that there are the correct number of rows
        cleaned_timestamp = data_cleaning(self.timetable)
        self.assertTrue(cleaned_timestamp.shape[0] == 192)





if __name__ == '__main__':
    unittest.main()
