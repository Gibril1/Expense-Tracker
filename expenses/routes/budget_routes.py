from flask import request
from flask_cors import cross_origin
from expenses import app, db
from models import Budget
from serializers import budget_schema, budgets_schema
import datetime

API_URL = '/api/budget'

@app.route(f'{API_URL}/create', methods=['POST'])
def create_budget():
    try:
        response = {
        'data':{},
        'error_message':''
        }

        # get request body
        data = request.json

        # check if amount has been supplied
        if not data['amount'] or not data['start_date'] or not data['days']:
            response['error_message'] = 'Please enter all fields'
            return response, 400
    
        budget = Budget(
            amount = data['amount'],
            category = data['category'],
            description = data['description'],
            start_date = datetime.datetime.utcnow(),
            end_date = datetime.datetime.utcnow()+datetime.timedelta(days=data['days'])
        )

        db.session.add(budget)
        db.session.commit()

        budget = budget_schema.dump(budget)
        response['data'] = budget
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route(f'{API_URL}/<int:id>', methods=['GET'])
def get_budget(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        budget = Budget.query.get(id=id)
        if not budget:
            response['error_message'] = f'Budget with id of { id } does not exist'
            return response, 400

        budget = budget_schema.dump(budget)
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['PUT'])
def update_budget(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        data = request.json

        budget = Budget.query.get(id=id)
        if not budget:
            response['error_message'] = f'Budget with id of { id } does not exist'
            return response, 400
        
        if data['start_date']:
            budget.start_date = data['start_date']
        if data['end_date']:
            budget.end_date = data['end_date']
        if data['amount']:
            budget.amount = data['amount']
        if data['category']:
            budget.category = data['category']
        
        budget = budget_schema.dump(budget)
        response['data'] = budget
        return response, 200
        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['DELETE'])
def delete_budget(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        

        budget = Budget.query.get(id=id)
        if not budget:
            response['error_message'] = f'Budget with id of { id } does not exist'
            return response, 400

        db.session.delete(budget)
        db.session.commit()

        response['data'] = id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500
