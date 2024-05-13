import os,sys
conf_path = os.getcwd()
sys.path.append(conf_path)


import pytest
from fastapi.testclient import TestClient
from main import app, BikeSearchService, BikeSearchParams
from time import strftime, localtime
from datetime import datetime, timedelta
from utilities import Utils

client = TestClient(app)

class TestBikeSearchService:

    @staticmethod
    def test_get_past_dates():
        # Test with valid inputs
        today = datetime.now().date() - timedelta(days=0)
        yest = datetime.now().date() - timedelta(days=1)
        assert Utils.get_past_dates("days", 1) == [yest,today]
        # Test with invalid inputs


    @staticmethod
    def test_epoch_to_date():
        #test_epoch_datetime = datetime(2024, 5, 12, 18, 46, 47, 952986)
        test_epoch = 1715519807
        test_date = '2024-05-12'
        assert Utils.epoch_to_date(test_epoch) ==test_date




