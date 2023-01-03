from flask_restful import Resource, reqparse, request
from src.db.src.receipt_calc import *

class Users(Resource):
    def get(self,user_id):
        """retrieves user info

        Args:
            user_id (str): id of user

        Returns:
            list: user id and user name
        """          
        res = getUser(user_id)
        return res
    
    def post(self):
        """creates user

        Returns:
            str: id of user
        """        
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str)
        args = parser.parse_args()
        user_name = args['user_name']

        res = addUser(user_name)
        return res

    def put(self,user_id):
        """edits user name

        Args:
            user_id (str): id of user

        Returns:
            str: new user name
        """            
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str)
        args = parser.parse_args()
        user_name = args['user_name']

        res = editUser(user_id,user_name)
        return res
    
    def delete(self,user_id):
        """removes user

        Args:
            user_id (str): id of user

        Returns:
            str: success/fail message
        """        
        res = removeUser(user_id)
        return res