



from datetime import date
from email.policy import default
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true

app = Flask(__name__)      # intialization of the Server
api = Api(app)     

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'                # Intialization of the database 
db = SQLAlchemy(app)

class HotelModel(db.Model):                           # Creating a DB object
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key =True)          # Primary true mean its going to be unique
    name = db.Column(db.String(100), nullable =False)     #nullable false means this field has to have  some information
    star = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable = False)
    city = db.Column(db.String(50), nullable = False)
    country = db.Column(db.String(50), nullable = False)
    hoteli = db.Column(db.String, nullable = False)
    facility1 = db.Column(db.String(50),default="None")
    facility2 = db.Column(db.String(50),default="None")
    facility3 = db.Column(db.String(50),default="None")
    avaliable_rooms = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.Integer, nullable =False, default = 1)

    

    def __repr__(self):                                     # to Show the data base as a String 
        return f"Hotel ( Name = {name}, star = {star}, price = {price}, city = {city}, country = {country}, hoteli = {hoteli}, facility1 = {facility1}, facility2 = {facility2}, facility3 = {facility3}, avaliable_rooms = {avaliable_rooms}, flag = {flag}" 

class ReservationModel(db.Model):
    __tablename__ =  'booking'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_name = db.Column(db.String, nullable =False)
    booked_room = db.Column(db.Integer, nullable = False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    relation = db.relationship("HotelModel")
    hotel_name = db.Column(db.String)

    
  #  def __init__(self, name, bookedroom, hotelid, hotelname):
  #      self.customer_name = name
   #     self.booked_room = bookedroom
    #    self.hotel_id = hotelid
     #   self.hotel_name = hotelname
        
    def json(self):
        return {'id': self.id,'Customer Name': self.customer_name, 'Hotel Name': self.hotel_name, 'Booked Rooms' : self.booked_room, 'Hotel ID' : self.hotel_id }
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(hotel_name=name).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


db.create_all()            # do it once to initialize it 

Hotel_put_agrs = reqparse.RequestParser()
Hotel_put_agrs.add_argument("name", type=str,help = "Name of the Hotel is required", required = True)
Hotel_put_agrs.add_argument("star", type=int, help = "Views of the Hotel")
Hotel_put_agrs.add_argument("price", type=int , help = "price on the Hotel")
Hotel_put_agrs.add_argument("city", type=str , help = "Name of the City")
Hotel_put_agrs.add_argument("country", type=str , help = "Name of the country")
Hotel_put_agrs.add_argument("hoteli", type=str , help = "Hotel of the hotel")
Hotel_put_agrs.add_argument("facility1", type=str , help = "write facility1")
Hotel_put_agrs.add_argument("facility2", type=str , help = "write facility2")
Hotel_put_agrs.add_argument("facility3", type=str , help = "write facility3")
Hotel_put_agrs.add_argument("avaliable_rooms", type=int, help = "Write rooms avaliable")

names = { "tim" : {"age":19 , "gender": "male" } , 
          "bilal" : {"age" : 20 , "gender": "male"}  }
Hotels = {}                          # Dictionary

resource_fields = {                   # To make your data output serializable
    'id': fields.Integer,
    'name' : fields.String,
    'star' : fields.Integer,
    'price' : fields.Integer,
    'city' : fields.String,
    'country' : fields.String,
    'hoteli' : fields.String,
    'facility1' : fields.String,
    'facility2' : fields.String,
    'facility3' : fields.String,
    'avaliable_rooms' : fields.Integer,

}

hotelb_put_args = reqparse.RequestParser()
hotelb_put_args.add_argument("hname",type=str, help = "entry the name of the hotel")
hotelb_put_args.add_argument("hid", type=int, help = "entry hotel id")
hotelb_put_args.add_argument("broom",type=int, help = "entry booked room", required = True)
hotelb_put_args.add_argument("cname",type=str, help = "entry customer name", required = True)



def abort_if_Hotel_does_not_exist(HotelID):    # to avoid  crashin if the Hotel id  does not exist
    if HotelID not in Hotels:
        abort(404, "Hotel id does not valid...")   # we need to send a status code with the message

def abort_if_Hotel_exist(HotelID):
    if HotelID in Hotels:
        abort (409, "Hotel id already exist")   #409 mean already exist
 
class HotelBooking(Resource):                   # Class created to handle get request from the resource 
    def get(Self, name):
        result = ReservationModel.find_by_name(name)
        if not result:
            abort(404, message= "Could not find Reservation with that ID")
        return result.json()
    
    def put(Self, name):
        args = hotelb_put_args.parse_args()
        result = HotelModel.query.filter_by(name=name).first()
        print(result.price)
        result1 = ReservationModel.find_by_name(name)
        if result1:
             abort(409, message = "Accomodation is booked .. ")
        booking = ReservationModel(customer_name = args['cname'],booked_room = args['broom'],hotel_id = result.id ,hotel_name = name)
        if result.avaliable_rooms >= args['broom']:
            result.avaliable_rooms = result.avaliable_rooms - args['broom']
        else:
            abort (404, message= "Room not avaliable")

        if result.avaliable_rooms <= 0:
            result.flag = 0


        db.session.add(result)
        db.session.commit()


        db.session.add(booking)
        db.session.commit()

        return booking.json()

    def delete(Self,name):
         item = ReservationModel.find_by_name(name)
         if item:
            item.delete_from_db()

         return {'message': 'Item deleted.'}

         



       
    
    def post (Self):
        return {"data": "posted"}

class HotelsAdd(Resource):
   
    @marshal_with(resource_fields)            # use it where every you want to serialize the output "result"
    def get(self, HotelID):
        result = HotelModel.query.filter_by(id=HotelID).filter_by(flag = 1).first()
        if not result:
            abort(404, message= "Could not find video with that ID")
        return result
        #abort_if_Hotel_does_not_exist(HotelID)
        #return Hotels[HotelID]

    @marshal_with(resource_fields)    
    def put(self, HotelID):             # there is a vedio ID of the record with the assosiated arguments "args"
     #   abort_if_Hotel_exist(HotelID)
        args = Hotel_put_agrs.parse_args()
        result = HotelModel.query.filter_by(id=HotelID).first()
        if result:
            abort(409, message = "ID already taken .. ")
        
        Hotels = HotelModel (id = HotelID, name= args['name'], star = args['star'], price = args['price'], city = args['city'], country = args['country'], hoteli = args['hoteli'], facility1 = args['facility1'], facility2 = args['facility2'], facility3 = args['facility3'], avaliable_rooms = args['avaliable_rooms'])
        db.session.add(Hotels)
        db.session.commit()
        return Hotels
     #   Hotels[HotelID] = args
     #   return Hotels[HotelID], 201     # there is a code you send with the output. 201 mean created 
        
    def delete(self, HotelID):
      #  abort_if_Hotel_does_not_exist(HotelID)
      result = HotelModel.query.filter_by(id=HotelID).first()
      if not result:
            abort(404, message = "record not found")
        
      db.session.delete(result)
      db.session.commit()
      return "deleted", 204

    def patch(self):     # to update a single record 
        return


class HotelList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = HotelModel.query.filter_by(flag = 1).first()
        return result



api.add_resource(HotelBooking, "/hotelbooking/<string:name>")    # from which root this resource can get accessed 

api.add_resource(HotelsAdd, "/hotels/<int:HotelID>")          # for Adding hotels

api.add_resource(HotelList, "/hotels/")                          # To get all hotels




if __name__ == "__main__":      # to behave it as a server 
    app.run(debug=True)

