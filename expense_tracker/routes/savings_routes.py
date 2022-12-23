from flask import request
from flask_cors import cross_origin
from expense_tracker import app, db
from expense_tracker.models import Savings, Goal
from expense_tracker.serializers import saving_schema, savings_schema
from expense_tracker.auth_middleware import token_required


import datetime

API_URL = '/api/savings'

@app.route(f'{API_URL}/create/<int:id>', methods=['POST'])
@token_required
def create_saving(user, id):
    try:
        response = {
        'data':{},
        'error_message':''
        }

        # data from request
        data = request.json

        if not data['amount']:
            response['error_message'] = 'Please enter the amount you want to save!'
            return response, 401

        goal = Goal.query.get(id)
        if not goal:
            response['error_message'] = f'Goal with id of {id} does not exist'
            return response, 401

        saving = Savings(
            user = user.id,
            goal = goal.id,
            amount = data['amount'],
            date_created = datetime.datetime.utcnow()
        )

        db.session.add(saving)
        db.session.commit()

        goal.savings_amount += data['amount']
        db.session.commit()

        saving = saving_schema.dump(saving)
        response['data'] = saving
        return response, 201
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['GET'])
@token_required
def get_saving(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        saving = Savings.query.get(id)
        if not saving:
            response['error_message'] = f'Saving with {id} id not found'
            return response, 400
        
        if user.id != saving.user:
            response['error_message'] = 'You are not authorised to get this saving'
            return response, 401

        saving = saving_schema.dump(saving)
        response['data'] = saving
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route(f'{API_URL}/<int:id>', methods=['PUT'])
@token_required
def update_saving(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        amount= request.json.get('amount')
    
        saving = Savings.query.get(id)
        if not saving:
            response['error_message'] = f'Saving with id of {id} not found'
            return response, 400
        
        if user.id != saving.user:
            response['error_message'] = 'You are not authorised to get this saving'
            return response, 401

        if amount:
            saving.amount = amount
        
        

        saving = saving_schema.dump(saving)
        response['data'] = saving
        return response, 200
    
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route(f'{API_URL}/<int:id>', methods=['DELETE'])
@token_required
def delete_saving(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        saving = Savings.query.get(id)
        if not saving:
            response['error_message'] = f'saving with {id} id not found'
            return response, 400
        
        if user.id != saving.user:
            response['error_message'] = 'You are not authorised to get this saving'
            return response, 401

        db.session.delete(saving)
        db.session.commit()

        response['data'] = id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/all/<int:id>', methods=['GET'])
@token_required
def get_savings(user, id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goal = Goal.query.get(id)
        if not goal:
            response['error_message'] = f'Goal with id of {id} does not exist'
            return response, 401

        savings = Savings.query.filter_by(goal=goal.id).all()
        savings = savings_schema.dump(savings)
        response['data'] = savings
        return response, 200
        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500