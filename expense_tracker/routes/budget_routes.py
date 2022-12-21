from flask import request
from expense_tracker import app, db
from expense_tracker.models import Budget
from expense_tracker.serializers import budget_schema, budgets_schema
from expense_tracker.auth_middleware import token_required
import datetime

API_URL = '/api/budget'

@app.route(f'{API_URL}/create', methods=['POST'])
@token_required
def create_budget(f):
    try:
        response = {
        'data':{},
        'error_message':''
        }

        # get request body
        data = request.json

        # check if amount has been supplied
        if not data['amount'] or not data['days']:
            response['error_message'] = 'Please enter all fields'
            return response, 400
    
        budget = Budget(
            amount = data['amount'],
            user= f.id,
            category = data['category'],
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
@token_required
def get_budget(f,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        budget = Budget.query.get(id)
        if not budget:
            response['error_message'] = f'Budget with id of { id } does not exist'
            return response, 400
        
        if f.id != budget.user:
            response['error_message'] = 'You are not authorized to get this budget'
            return response, 401

        budget = budget_schema.dump(budget)
        response['data'] = budget
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['PUT'])
@token_required
def update_budget(f,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        start_date= request.json.get('start_date')
        end_date= request.json.get('end_date')
        amount= request.json.get('amount')
        category= request.json.get('category')

        budget = Budget.query.get(id)
        if not budget:
            response['error_message'] = f'Budget with id of { id } does not exist'
            return response, 400

        if f.id != budget.user:
            response['error_message'] = 'You are not authorized to update this budget'
            return response, 401

        if start_date:
            budget.start_date = start_date
        if end_date:
            budget.end_date = end_date
        if amount:
            budget.amount = amount
        if category:
            budget.category = category
        
        budget = budget_schema.dump(budget)
        response['data'] = budget
        return response, 200
        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['DELETE'])
@token_required
def delete_budget(f,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        

        budget = Budget.query.get(id)
        if not budget:
            response['error_message'] = f'Budget with id of { id } does not exist'
            return response, 400
        
        if f.id != budget.user:
            response['error_message'] = 'You are not authorized to get this budget'
            return response, 401

        db.session.delete(budget)
        db.session.commit()

        response['data'] = id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route(f'{API_URL}/', methods=['GET'])
@token_required
def get_budgets(f):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        budgets = Budget.query.filter_by(user=f.id).all()
        budgets = budgets_schema.dump(budgets)
        response['data'] = budgets
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500
