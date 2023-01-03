from src.receipt_calc import *
from src.db_utils import *

""" table building """
def insertTestData():
    """inserts test data into tables
    """
    exec_sql_file("../tests/seed_data.sql")  

def rebuildTablesWithTestData():
    buildTables()
    insertTestData()