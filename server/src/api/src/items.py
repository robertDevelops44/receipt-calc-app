from flask_restful import Resource, reqparse, request
from src.db.src.receipt_calc import *

class Items(Resource):
    def post(self):
        """creates item

        Returns:
            str: id of item
        """        
        parser = reqparse.RequestParser()
        parser.add_argument('store', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('tax', type=str)
        parser.add_argument('cost', type=str)
        args = parser.parse_args()
        store = args['store']
        name = args['name']
        tax = args['tax']
        cost = args['cost']

        res = addItem(store,name,tax,cost)
        return res

