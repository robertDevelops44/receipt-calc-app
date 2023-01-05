import math
from .db_utils import *

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
    res = exec_commit_returning_one(sql, args)
    return res

def removeUser(user_id:str):
    """removes a user from users table
        removes owner assignments with user
            updates items from owner assignments to new cost per user

    Args:
        user_id (str): id of user

    Returns:
        str: success/fail message
    """    
    owners = getAssignments(user_id)
    sql = """DELETE FROM users WHERE id = %(user_id)s ;
                DELETE FROM owners WHERE user_id = %(user_id)s ;"""
    for assignment in owners:
        item_id = assignment[1]
        update_query = """UPDATE items SET cost_per_user = 
                            ROUND(((SELECT total_cost FROM items WHERE id = {item_id}) / (SELECT COUNT(*) FROM owners WHERE item_id = {item_id}))::numeric, 2) 
                                WHERE id = {item_id} ;""".format(item_id=item_id)
        sql += update_query
    args = {'user_id': user_id}
    try:
        exec_commit(sql,args)
        return "Successfully deleted user"
    except:
        return "Failed to delete user"

def editUser(user_id:str, name:str):    
    """edits user name

    Args:
        user_id (str): id of user
        name (str): new name to edit to

    Returns:
        str: new name
    """    
    sql = """UPDATE users SET name = %(name)s WHERE id = %(user_id)s RETURNING name ;"""
    args = {'user_id':user_id, 'name':name}
    res = exec_commit_returning_one(sql,args)
    return res

def addItem(store:str, name:str, tax:str, cost:str):
    """adds an item to items table

    Args:
        store (str): name of store
        name (str): name of item
        tax (str): tax applied to item
        cost (str): cost of item

    Returns:
        str: item_id
    """    
    sql = """INSERT INTO items (store,name,tax,total_cost,cost_per_user) VALUES (%s, %s, %s, %s, %s) RETURNING id;"""
    total_cost = math.floor((float(cost) * (1 + (float(tax)/100)))*100)/100
    args = [store,name,tax,total_cost,total_cost]
    res = exec_commit_returning_one(sql, args)
    return res

def removeItem(item_id:str):
    """removes an item from items table
        removes assignments from owners table related to item

    Args:
        item_id (str): id of item to be removed

    Returns:
        str: success/fail message
    """    
    sql = """DELETE FROM items WHERE id = %(item_id)s ;
                DELETE FROM owners WHERE item_id = %(item_id)s ;"""
    args = {'item_id':item_id}
    try:
        exec_commit(sql,args)
        return "Successfully deleted item"
    except:
        return "Failed to delete item"

def editItem(item_id:str, store:str,name:str,tax:str,total_cost:str,cost_per_user:str):
    """edits info of an item

    Args:
        item_id (str): id of item
        store (str): store name
        name (str): item name
        tax (str): tax rate of item
        total_cost (str): total cost of item
        cost_per_user (str): cost per user of item

    Returns:
        str: success/fail message
    """    
    sql = """UPDATE items SET 
                store = %s, name = %s, tax = %s, total_cost = %s, cost_per_user = %s WHERE id = %s RETURNING name ;"""
    args = [store,name,tax,total_cost,cost_per_user,item_id]
    try:
        exec_commit(sql,args)
        return "Successfully edited item"
    except:
        return "Failed to edit item"


def assignOwner(user_id:str, item_id:str):
    """places an owner assignment of a user_id & item_id relationship in owners table

    Args:
        user_id (str): id of user
        item_id (str): id of item

    Returns:
        str: success/fail message
    """    
    ownerExists = checkOwnerExists(user_id,item_id)
    if ownerExists == False:
        sql = """INSERT INTO owners (user_id, item_id) VALUES (%(user_id)s, %(item_id)s) ;
                    UPDATE items SET cost_per_user = 
                        ROUND(((SELECT total_cost FROM items WHERE id = %(item_id)s) / (SELECT COUNT(*) FROM owners WHERE item_id = %(item_id)s))::numeric, 2) 
                            WHERE id = %(item_id)s ;
                        SELECT id FROM owners WHERE user_id = %(user_id)s AND item_id = %(item_id)s ;"""
        args = {'user_id':user_id, 'item_id':item_id}
        try:
            res = exec_commit_returning_one(sql,args)
            return res[0]
        except:
            return "Failed to assign owner"
    else:
        return "Owner assignment already exists"

def removeOwner(owner_id:str):
    """removes an owner record from owners table with matching user_id & item_id

    Args:
        user_id (str): id of user
        item_id (str): id of item

    Returns:
        str: success/fail message
    """    
    sql = """UPDATE items SET cost_per_user = 
                ROUND(((SELECT total_cost FROM items WHERE id = (SELECT item_id FROM owners WHERE id = %(owner_id)s) ) / 
                        ((SELECT COUNT(*) FROM owners WHERE item_id = (SELECT item_id FROM owners WHERE id = %(owner_id)s)) - 1))::numeric, 2) 
                            WHERE id = (SELECT item_id FROM owners WHERE id = %(owner_id)s) ;
                DELETE FROM owners WHERE id = %(owner_id)s ; """
    args = {'owner_id':owner_id}
# try:
    exec_commit(sql,args)
    return "Successfully removed owner"
# except:
    # return "Failed to remove owner"


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
    """retrieves item

    Args:
        item_id (str): id of item

    Returns:
        tuple: id, store, name, tax, total cost, cost per user
    """    
    sql = """SELECT row_to_json(the_item) FROM (SELECT * FROM items WHERE id = %s)the_item ;"""
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
    sql = """SELECT ROUND((SUM(user_total.final_costs))::numeric,2) FROM (SELECT (items.cost_per_user * (1 + (items.tax / 100))) AS final_costs FROM (owners INNER JOIN items ON owners.item_id = items.id) WHERE owners.user_id = %s)user_total ;"""
    args = [user_id]
    res = exec_get_one(sql, args)
    return float(res[0])

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

def checkOwnerExists(user_id:str,item_id:str):
    """checks if owner assignment pair exists

    Args:
        user_id (str): id of user
        item_id (str): id of item

    Returns:
        bool: true/false
    """    
    sql = """SELECT COUNT(*) FROM owners WHERE user_id = %s AND item_id = %s ;"""
    args = [user_id,item_id]
    res = exec_get_one(sql, args)
    if res[0] == 0:
        return False
    else:
        return True

def getOwnerAssignment(owner_id):
    """retrieves owner assignment pair

    Args:
        owner_id (str): id of owner

    Returns:
        list: tuples of assignment pairs
    """    
    sql = """SELECT row_to_json(the_owner) FROM (SELECT * FROM owners WHERE id = %s)the_owner ;"""
    args = [owner_id]
    res = exec_get_all(sql, args)
    return res

def getUser(user_id):
    """retrieves user id and user name from user_id

    Args:
        user_id (str): id of user

    Returns:
        list: user id and user name
    """    
    sql = """SELECT row_to_json(the_user) FROM (SELECT * FROM users WHERE id = %s)the_user ;"""
    args = [user_id]
    res = exec_get_all(sql, args)
    return res[0]

def getAssignments(user_id):
    """retrieves all owners

    Returns:
        _type_: _description_
    """    
    sql = """SELECT user_id,item_id FROM owners WHERE user_id = %s;"""
    args = [user_id]
    res = exec_get_all(sql,args)
    return res

def checkUserExists(user_id):
    """checks if user exists

    Args:
        user_id (str): id of user

    Returns:
        bool: true/false
    """    
    sql = """SELECT COUNT(*) FROM users WHERE id = %s ;"""
    args = [user_id]
    res = exec_get_one(sql, args)
    if res[0] == 0:
        return False
    else:
        return True