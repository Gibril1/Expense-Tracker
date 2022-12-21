from expense_tracker import app
from flask import request, jsonify
from functools import wraps
from expense_tracker.models import Users

import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({ 'message': 'Token not supplied'}), 401
        # print(token)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # print(data)
            user = Users.query.get(data['user'])
            # print(user)
        except:
            return jsonify({
                'message': 'Token is invalid'
            }), 401

        
        
        return f(user, *args, **kwargs)
    return decorated

        