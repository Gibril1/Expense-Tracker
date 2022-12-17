from flask import request
from expenses import app, bcrypt, db
from models import Users
from serializers import user_schema
import jwt
import datetime

@app.route('/', methods=['POST'])
def register():
    try:
        response = {
            'data':{},
            'error_message':''
        }

        data = request.json

        if not data['username'] or not data['password']:
            response['error_message'] = 'Please enter all fields'
            return response, 404
        
        # check if user already exists
        user = Users.query.filter_by(username=data['username']).first()
        if user:
            response['error_message'] = 'User account already exists. Login'
            return response, 400
        

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # commit user into the database
        user = Users(
            username=data['username'],
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        user = user_schema.dump(user)
        response['data'] = user
        return response, 201
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route('/login', methods=['POST'])
def login():
    try:
        response = {
            'data':{},
            'error_message':''
        }

        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            response['error_message'] = 'Please enter all fields'
            return response, 404
        
        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'user':user.username,'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            response['data']['token'] = token

            user = user_schema.dump(user)
            response['data']['user'] = user

            return response , 200
        else:
            response['error_message'] = 'Invalid credentials'
            return response, 200



        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500