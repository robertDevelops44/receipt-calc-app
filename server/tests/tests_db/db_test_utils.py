from src.db.src.receipt_calc import *
from src.db.src.db_utils import *

""" table building """
def insertTestData():
    """inserts test data into tables
    """
    exec_sql_file("../../../tests/tests_db/seed_data.sql")  

def rebuildTablesWithTestData():
    buildTables()
    insertTestData()