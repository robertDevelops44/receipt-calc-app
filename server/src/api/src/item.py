from flask_restful import Resource, reqparse, request
from src.db.src.receipt_calc import *

class Item(Resource):
    def get(self,item_id):
        """retrieves item info

        Args:
            item_id (str): id of item

        Returns:
            list: item info
        """          
        res = getItem(item_id)
        return res

    def put(self,item_id):
        """edits item info

        Args:
            item_id (str): id of item

        Returns:
            str: success/fail message
        """            
        parser = reqparse.RequestParser()
        parser.add_argument('store', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('tax', type=str)
        parser.add_argument('cost', type=str)
        parser.add_argument('cost_per_user', type=str)
        args = parser.parse_args()
        store = args['store']
        name = args['name']
        tax = args['tax']
        cost = args['cost']
        cost_per_user = args['cost_per_user']


        res = editItem(item_id,store,name,tax,cost,cost_per_user)
        return res
    
    def delete(self,item_id):
        """removes item

        Args:
            item_id (str): id of item

        Returns:
            str: success/fail message
        """        
        res = removeItem(item_id)
        return res