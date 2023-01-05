from flask_restful import Resource, reqparse, request
from src.db.src.receipt_calc import *

class Owners(Resource):
    def get(self):
        """retrieves all owner assignments

        Returns:
            list: owner pairs
        """        
        res = getAssignments()
        return res

    def post(self):
        """creates owner assignment

        Returns:
            str: success/fail message
        """        
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('item_id', type=str)
        args = parser.parse_args()
        user_id = args['user_id']
        item_id = args['item_id']

        res = assignOwner(user_id,item_id)
        return res


