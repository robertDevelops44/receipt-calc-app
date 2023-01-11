from flask_restful import Resource, reqparse, request
from src.db.src.receipt_calc import *

class UserTotal(Resource):
    def get(self,user_id):
        """retrieves total cost of a user

        Args:
            user_id (str): id of user

        Returns:
            str: total cost
        """          
        res = getUserTotal(user_id)
        return res