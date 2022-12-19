from flask import request
from flask_cors import cross_origin
from expenses import app, db
from models import Expenses
from serializers import expenses_schema, expensess_schema
import datetime

@app.route('/create-expenses', methods=['POST'])
def create_expenses():
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
    
        expenses = Expenses(
            amount = data['amount'],
            category = data['category'],
            description = data['description'],
            date = datetime.datetime.utcnow()
        )

        db.session.add(expenses)
        db.session.commit()

        expenses = expenses_schema.dump(expenses)
        response['data'] = expenses
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route('/expenses/<int:id>', methods=['GET'])
@cross_origin
def get_expenses(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        expenses = Expenses.query.get(id=id)
        if not expenses:
            response['error_message'] = f'expenses with id of { id } does not exist'
            return response, 400

        expenses = expenses_schema.dump(expenses)
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route('/expenses/<int:id>', methods=['PUT'])
@cross_origin
def update_expenses(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        data = request.json

        expenses = Expenses.query.get(id=id)
        if not expenses:
            response['error_message'] = f'Expenses with id of { id } does not exist'
            return response, 400
        
        if data['amount']:
            expenses.amount = data['amount']
        if data['category']:
            expenses.category = data['category']
        if data['description']:
            expenses.description = data['description']
        
        expenses.date = datetime.datetime.utcnow()

        expenses = expenses_schema.dump(expenses)
        response['data'] = expenses
        return response, 201

    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route('/expenses/<int:id>', methods=['DELETE'])
@cross_origin
def delete_expenses(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        expenses = Expenses.query.get(id=id)
        if not expenses:
            response['error_message'] = f'expenses with id of { id } does not exist'
            return response, 400
        
        db.session.delete(expenses)
        db.session.commit()

        response['data'] = expenses.id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route('/expensess', methods=['GET'])
def get_expensess():
    try:
        response = {
            'data':{},
            'error_message':''
        }

        expensess = Expenses.query.all()

        expensess = expensess_schema.dump(expensess)
        response['data'] = expensess
        return response, 200

    except Exception as e:
        response['error_message'] = str(e)
        return response, 500