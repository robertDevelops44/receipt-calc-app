import unittest
import json
from src.db.src.receipt_calc import *
from tests.tests_db.db_test_utils import *
from tests.tests_api.api_test_utils import *

class TestReceiptCalcApi(unittest.TestCase):
    def setUp(self):
        rebuildTablesWithTestData()

    def test_get_user(self):
        """tests retrieving a user with a GET call
        """        
        actual = get_rest_call(self, "http://localhost:5000/user/1")
        expected = [{'id': 1, 'name': 'Bob'}]
        self.assertEqual(actual,expected)
    
    def test_post_user(self):
        """tests creating a user with a POST call
        """        
        data = dict(user_name = "Mike")
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        post_rest_call(self,"http://localhost:5000/users",jdata,hdr)

        res = get_rest_call(self, "http://localhost:5000/user/4")
        actual = res 
        expected = [{'id': 4, 'name': 'Mike'}]
        self.assertEqual(actual,expected)
    
    def test_put_user(self):
        data = dict(user_name = "Bobster")
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        put_rest_call(self,"http://localhost:5000/user/1",jdata,hdr)

        res = get_rest_call(self, "http://localhost:5000/user/1")
        actual = res
        expected = [{'id': 1, 'name': 'Bobster'}]
        self.assertEqual(actual,expected)
    
    def test_delete_user(self):
        put_rest_call(self,"http://localhost:5000/user/1")

        res = get_rest_call(self, "http://localhost:5000/user/1")
        actual = res 
        expected = [{'id': 1, 'name': None}]
        self.assertEqual(actual,expected)




