from flask_restful import Resource, reqparse, request
from src.db.src.receipt_calc import *

class Owner(Resource):
    def get(self,owner_id):
        """retrieves owner info

        Args:
            owner_id (str): id of owner

        Returns:
            list: owner assignment info - user_id and item_id
        """          
        res = getOwnerAssignment(owner_id)
        return res
    
    def delete(self,owner_id):
        """removes owner assignment

        Args:
            owner_id (str): id of owner

        Returns:
            str: success/fail message
        """        
        res = removeOwner(owner_id)
        return res
