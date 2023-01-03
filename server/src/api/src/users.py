from flask_restful import Resource, reqparse, request
from src.db.src.receipt_calc import *

class Users(Resource):
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

