from flask_restful import Resource, reqparse, request
from db.src.receipt_calc import *

class Users(Resource):
    def get(self,user_id):
        """retrieves user
        """        
        res = getUser(user_id)
        return res
    
    def post(self):
        """creates user with given name
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str)
        args = parser.parse_args()
        user_name = args['user_name']

        res = addUser(user_name)
        return res