import unittest
from src.db.src.receipt_calc import *
from tests.tests_db.db_test_utils import *
from tests.tests_api.api_test_utils import *

class TestReceiptCalcApi(unittest.TestCase):
    def setUp(self):
        rebuildTablesWithTestData()

    def test_get_user(self):
        actual = get_rest_call(self, "http://localhost:5000/users/1")
        expected = [{'id': 1, 'name': 'Bob'}]
        self.assertEqual(actual,expected)