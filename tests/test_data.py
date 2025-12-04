'''A unit test for the data module.'''
# use plain python , so that this file can be run
from turtle import st
import unittest
import pandas as pd
from modules.dataset import load_survey

class TestDataModule(unittest.TestCase):
    '''Tests for the data module.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.df = load_survey()

    def test_load_survey(self):
        '''Test loading the survey data.'''
        df = load_survey(key='test')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        for col in ["BPM", "anxiety", "Depression"]:
            self.assertIn(col, df.columns)

