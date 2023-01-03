import unittest
from db.src.receipt_calc import *
from db.tests.db_test_utils import *
from api_test_utils import *

class TestReceiptCalcApi(unittest.TestCase):
    def setUp(self):
        rebuildTablesWithTestData()

    def test_get_user(self):
        actual = get_rest_call(self, "http://localhost:5000/users/1")
        expected = ""
        self.assertEqual(actual,expected)