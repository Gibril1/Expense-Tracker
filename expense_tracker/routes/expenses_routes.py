from flask import request
from flask_cors import cross_origin
from expense_tracker import app, db
from expense_tracker.models import Expenses, Budget
from expense_tracker.serializers import expenses_schema, expensess_schema
from expense_tracker.auth_middleware import token_required
import datetime

API_URL = '/api/expenses'



@app.route(f'{API_URL}/create/<int:id>', methods=['POST'])
@token_required
def create_expenses(user, id):
    try:
        response = {
        'data':{},
        'error_message':''
        }

        # get request body
        data = request.json

        # check if amount has been supplied
        if not data['amount']:
            response['error_message'] = 'Amount has not been specified'
            return response, 400

        # get the specific budget in which this expense is being deducted from
        budget = Budget.query.get(id)

        if not budget:
            response['error_message'] = f'Budget with id of {id} does not exist'
            return response, 400

        # making entries into the database
        expenses = Expenses(
            amount = data['amount'],
            user = user.id,
            budget = budget.id,
            category = data['category'],
            description = data['description'],
            date = datetime.datetime.utcnow()
        )
        db.session.add(expenses)
        db.session.commit()

        budget.remainder += data['amount']

        # checking to see if the expenses have exceeded the set budget
        budget.status = True if budget.remainder > budget.amount else False

    

        db.session.commit()
        

        expenses = expenses_schema.dump(expenses)
        response['data'] = expenses
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route(f'{API_URL}/<int:id>', methods=['GET'])
@token_required
def get_expenses(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        expenses = Expenses.query.get(id)
        if not expenses:
            response['error_message'] = f'Expenses with id of { id } does not exist'
            return response, 400
        
        if user.id != expenses.user:
            response['error_message'] = 'You are not authorized to get this expenses'
            return response, 401


        expenses = expenses_schema.dump(expenses)
        response['data'] = expenses
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['PUT'])
@token_required
def update_expenses(user, id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        amount = request.json.get('amount')
        category = request.json.get('category')
        description = request.json.get('description')

        expenses = Expenses.query.get(id)
        if not expenses:
            response['error_message'] = f'Expenses with id of { id } does not exist'
            return response, 400

        if user.id != expenses.user:
            response['error_message'] = 'You are not authorized to get this expenses'
            return response, 401
        
        if amount:
            expenses.amount = amount
        if category:
            expenses.category = category
        if description:
            expenses.description = description
                                                      
        expenses.date = datetime.datetime.utcnow()

        db.session.commit()

        expenses = expenses_schema.dump(expenses)
        response['data'] = expenses
        return response, 201

    except Exception as e:
        response['error_message'] = (e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['DELETE'])
@token_required
def delete_expenses(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        expenses = Expenses.query.get(id)
        if not expenses:
            response['error_message'] = f'Expenses with id of { id } does not exist'
            return response, 400

        if user.id != expenses.user:
            response['error_message'] = 'You are not authorized to get this expenses'
            return response, 401
        
        db.session.delete(expenses)
        db.session.commit()

        response['data'] = id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/all/<int:id>', methods=['GET'])
@token_required
def get_expensess(user, id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        budget = Budget.query.get(id)
        if not budget:
            response['error_message'] = f'Budget with id of {id} does not exist'
            return response, 400

        if user.id != budget.user:
            response['error_message'] = 'You are not authorized'
            return response, 401

        expensess = Expenses.query.filter_by(budget=budget.id).all()

        expensess = expensess_schema.dump(expensess)
        response['data'] = expensess
        return response, 200

    except Exception as e:
        response['error_message'] = str(e)
        return response, 500