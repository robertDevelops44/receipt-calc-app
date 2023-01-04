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
        delete_rest_call(self,"http://localhost:5000/user/1")

        user_count = exec_get_one('SELECT COUNT(*) FROM users')

        actual = user_count[0]
        expected = 2
        self.assertEqual(actual,expected)

    def test_get_item(self):
        """tests retrieving a item with a GET call
        """        
        actual = get_rest_call(self, "http://localhost:5000/item/1")
        expected = [{'cost_per_user': 12.99,'id': 1,'name': 'Swifter','store': 'Walmart','tax': 8,'total_cost': 12.99}]
        self.assertEqual(actual,expected)
    
    def test_post_item(self):
        """tests creating a item with a POST call
        """        
        data = dict(store = "CVS", name = "Tylenol",  tax = 8, cost = 8.62)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        post_rest_call(self,"http://localhost:5000/items",jdata,hdr)

        res = get_rest_call(self, "http://localhost:5000/item/4")
        actual = res 
        expected = [{'cost_per_user': 9.3,'id': 4,'name': 'Tylenol','store': 'CVS','tax': 8,'total_cost': 9.3}]
        self.assertEqual(actual,expected)
    
    def test_put_item(self):
        data = dict(store = "Target", name = "Potats",  tax = 8, cost = 9.99, cost_per_user = 9.99)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        put_rest_call(self,"http://localhost:5000/item/2",jdata,hdr)

        res = get_rest_call(self, "http://localhost:5000/item/2")
        actual = res
        expected = [{'cost_per_user': 9.99,'id': 2,'name': 'Potats','store': 'Target','tax': 8,'total_cost': 9.99}]
        self.assertEqual(actual,expected)
    
    def test_delete_item(self):
        delete_rest_call(self,"http://localhost:5000/item/1")

        item_count = exec_get_one('SELECT COUNT(*) FROM items')
        
        actual = item_count[0]
        expected = 2
        self.assertEqual(actual, expected)


