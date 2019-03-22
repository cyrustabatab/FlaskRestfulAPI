from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank")
    parser.add_argument('store_id',type=int,required=True,help="This field cannot be left blank")

    @jwt_required()
    def get(self,name):
        
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': 'Item Not Found'}

    
    def post(self,name):
        
    
        if ItemModel.find_by_name(name):
            return {"message": "item already exists"}

        data = Item.parser.parse_args() 
        item = ItemModel(name,**data)
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"},500

        return item.json(),201



    def delete(self,name):
       
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            message = {"message": "Item deleted"}
        else:
            message= {"message": "Item does not exist"}

        return message
    
    


    def put(self,name):
        """create or update exisitng itme"""


        data = Item.parser.parse_args() 
        
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']

        try:
            item.save_to_db()
        except:
            return {"message": "could not update item"},500

        return item.json()        



class ItemList(Resource):


    def get(self):
        
        return {'items': [item.json() for item in ItemModel.query.all()]}
