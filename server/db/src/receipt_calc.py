import math
import os
from turtle import update
from src.db_utils import *


"""TABLE BUILDING"""

def buildTables():
    """constructs empty tables
    """    
    exec_sql_file("../src/data.sql")  


"""MODIFIERS"""

def addUser(name:str):
    """adds a user to users table

    Args:
        name (str): name of user

    Returns:
        str: user_id
    """    
    sql = """INSERT INTO users (name) VALUES (%s) RETURNING id;"""
    args = [name]
    res = exec_insert_returning(sql, args)
    return res

def addItem(store:str, name:str, cost:str, tax:str):
    """adds an item to items table

    Args:
        store (str): name of store
        name (str): name of item
        cost (str): cost of item
        tax (str): tax applied to item

    Returns:
        str: item_id
    """    
    sql = """INSERT INTO items (store,name,tax,total_cost,cost_per_user) VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
    total_cost = math.floor((cost * (1 + (tax/100)))*100)/100
    args = [store,name,tax,total_cost,total_cost]
    res = exec_insert_returning(sql, args)
    return res

def removeItem(item_id:str):
    """removes an item from items table
        removes assignments from owners table related to item

    Args:
        item_id (str): id of item to be removed

    Returns:
        str: success/fail message
    """    
    sql = """DELETE FROM items WHERE id = %s ;
                DELETE FROM owners WHERE item_id = %s ;"""
    args = [item_id, item_id]
    try:
        exec_commit(sql,args)
        return "Successfully deleted item"
    except:
        return "Failed to delete item"

def assignOwner(user_id:str, item_id:str):
    """places an owner assignment of a user_id & item_id relationship in owners table

    Args:
        user_id (str): id of user
        item_id (str): id of item

    Returns:
        str: success/fail message
    """    
    ownerExists = ownerAssignmentExists(user_id,item_id)
    if ownerExists == False:
        sql = """INSERT INTO owners (user_id, item_id) VALUES (%s, %s) ;
                    UPDATE items SET cost_per_user = 
                        ROUND(((SELECT total_cost FROM items WHERE id = %s) / (SELECT COUNT(*) FROM owners WHERE item_id = %s))::numeric, 2) 
                            WHERE id = %s ;"""
        args = [user_id, item_id, item_id, item_id, item_id]
        try:
            exec_commit(sql,args)
            return "Successfully assigned owner"
        except:
            return "Failed to assign owner"
    else:
        return "Owner assignment already exists"

def removeOwner(user_id:str, item_id:str):
    """removes an owner record from owners table with matching user_id & item_id

    Args:
        user_id (str): id of user
        item_id (str): id of item

    Returns:
        str: success/fail message
    """    
    sql = """DELETE FROM owners WHERE user_id = %s AND item_id = %s ;                
                UPDATE items SET cost_per_user = 
                    ROUND(((SELECT total_cost FROM items WHERE id = %s) / (SELECT COUNT(*) FROM owners WHERE item_id = %s))::numeric, 2) 
                        WHERE id = %s ;"""
    args = [user_id, item_id, item_id, item_id, item_id]
    try:
        exec_commit(sql,args)
        return "Successfully removed owner"
    except:
        return "Failed to remove owner"


"""ACCESSORS"""

def getUserName(user_id:str):
    """retrieves user name from user_id

    Args:
        user_id (str): id of user

    Returns:
        str: user's name
    """    
    sql = """SELECT name FROM users WHERE id = %s ;"""
    args = [user_id]
    res = exec_get_one(sql, args)
    return res[0]

def getItem(item_id:str):
    sql = """SELECT * FROM items WHERE id = %s ;"""
    args = [item_id]
    res = exec_get_all(sql, args)
    return res[0]

def getUserTotal(user_id:str):
    """retrieves total of a user

    Args:
        user_id (str): id of user

    Returns:
        str: total of user
    """    
    sql = """SELECT SUM(items.total_cost) AS user_total FROM (owners INNER JOIN items ON owners.item_id = items.id) WHERE owners.user_id = %s ;"""
    args = [user_id]
    res = exec_get_one(sql, args)
    return res

def getItemTotalCost(item_id:str):
    """retrieves total cost of an item

    Args:
        item_id (str): id of item

    Returns:
        str: total cost of an item
    """    
    sql = """SELECT total_cost FROM items WHERE id = %s ;"""
    args = [item_id]
    res = exec_get_one(sql, args)
    return res[0]

def getItemCostPerUser(item_id:str):
    """retrieves the cost per user of an item

    Args:
        item_id (str): id of item

    Returns:
        str: cost per user of an item
    """    
    sql = """SELECT cost_per_user FROM items WHERE id = %s ;"""
    args = [item_id]
    res = exec_get_one(sql, args)
    return res[0]

def ownerAssignmentExists(user_id:str,item_id:str):
    sql = """SELECT COUNT(*) FROM owners WHERE user_id = %s AND item_id = %s ;"""
    args = [user_id,item_id]
    res = exec_get_one(sql, args)
    if res[0] == 0:
        return False
    else:
        return True

def getOwnerAssignment(owner_id):
    sql = """SELECT * FROM owners WHERE id = %s ;"""
    args = [owner_id]
    res = exec_get_all(sql, args)
    return res
