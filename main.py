import requests
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, marshal_with, fields, abort
from flask_sqlalchemy import SQLAlchemy
import jwt
from functools import wraps


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'sekretniy'

db = SQLAlchemy(app)

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    "frm", type=str, help='From which city', required=True)
post_parser.add_argument("to", type=str, help='To which city', required=True)
post_parser.add_argument("departure", type=str,
                         help='Departure time', required=True)
post_parser.add_argument(
    "arrival", type=str, help='Arrival time', required=True)
post_parser.add_argument("airplane", type=str,
                         help='Airplane information', required=True)
post_parser.add_argument("passengers", type=int,
                         help='Passengers number', required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument(
    "frm", type=str, help='From which city')
put_parser.add_argument("to", type=str, help='To which city')
put_parser.add_argument("departure", type=str,
                        help='Departure time')
put_parser.add_argument(
    "arrival", type=str, help='Arrival time')
put_parser.add_argument("airplane", type=str,
                        help='Airplane information')
put_parser.add_argument("passengers", type=int,
                        help='Passengers number')

resource_fields = {
    'frm': fields.String,
    'to': fields.String,
    'departure': fields.String,
    'arrival': fields.String,
    'airplane': fields.String,
    'passengers': fields.Integer
}


class Flights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frm = db.Column(db.String(30))
    to = db.Column(db.String(30))
    departure = db.Column(db.String(30))
    arrival = db.Column(db.String(30))
    airplane = db.Column(db.String(30))
    passengers = db.Column(db.Integer)


class Admin(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Admin.query.filter_by(
                username=data['username'], password=data['password']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


class Flight(Resource):

    @token_required
    def delete(self, current_user, from_city, to_city):
        data = Flights.query.filter_by(frm=from_city, to=to_city).first()
        if not data:
            return "Flight not found", 404
        db.session.delete(data)
        db.session.commit()

        return "Flight succesfully deleted!"

    @token_required
    def put(self, current_user, from_city, to_city):
        args = put_parser.parse_args()
        data = Flights.query.filter_by(frm=from_city, to=to_city).first()
        if not data:
            return "Flight not found", 404
        if args['frm']:
            data.frm = args['frm']
        if args['to']:
            data.to = args['to']
        if args['departure']:
            data.departure = args['departure']
        if args['arrival']:
            data.arrival = args['arrival']
        if args['airplane']:
            data.airplane = args['airplane']
        if args['passengers']:
            data.passengers = args['passengers']

        db.session.commit()

        return "Flight succesfully updated!"

    @marshal_with(resource_fields)
    def get(self, from_city, to_city):
        data = Flights.query.filter_by(frm=from_city, to=to_city).all()
        if not data:
            abort(404, message='Flight not found')
        return data


class PostFlight(Resource):

    @token_required
    def post(self, current_user):
        args = post_parser.parse_args()
        flight = Flights(frm=args['frm'],
                         to=args['to'],
                         departure=args['departure'],
                         arrival=args['arrival'],
                         airplane=args['airplane'],
                         passengers=args['passengers'])
        db.session.add(flight)
        db.session.commit()
        return 'Flight succesfully added', 201


class AAAdmin(Resource):
    def get(self):
        auth = request.authorization
        print(auth)
        if not auth or not auth.username or not auth.password:
            abort(400, message='Bad request')
        admin = Admin.query.filter_by(username=auth.username).first()
        if not admin:
            abort(404, message='Admin not found')
        if auth.password == admin.password:
            token = jwt.encode({'username': admin.username,
                                'password': admin.password}, app.config['SECRET_KEY'])
            return token
        else:
            abort(401, message='Wrong password')


class EndFlight(Resource):
    def get(self):
        pass


api.add_resource(Flight, "/flights/<string:from_city>/<string:to_city>")
api.add_resource(PostFlight, '/flights')
api.add_resource(AAAdmin, '/authentication_authorization')
api.add_resource(EndFlight, '/end_session')


def main():

    app.run(debug=True)


if __name__ == '__main__':
    main()
