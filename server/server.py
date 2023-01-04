from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from src.db.src.db_utils import *
from src.api.src.users import *
from src.api.src.user import *
from src.api.src.items import *
from src.api.src.item import *

app = Flask(__name__) #create Flask instance
CORS(app) #Enable CORS on Flask server to work with Nodejs pages
api = Api(app) #api router
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:item_id>')

if __name__ == '__main__':
    print("Loading db");
    exec_sql_file('data.sql');
    print("Starting flask");
    app.run(debug=True), #starts Flask



    