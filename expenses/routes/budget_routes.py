from flask import request
from flask_cors import cross_origin
from expenses import app, db
from models import Budget
from serializers import budget_schema, budgets_schema
import datetime

@app.route('/create-budget', methods=['POST'])
def create_budget():
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
    
        budget = Budget(
            amount = data['amount'],
            category = data['category'],
            description = data['description'],
            date = datetime.datetime.utcnow()
        )

        db.session.add(budget)
        db.session.commit()

        budget = budget_schema.dump(budget)
        response['data'] = budget
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route('/budget/<int:id>', methods=['GET'])
@cross_origin
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

@app.route('/budget/<int:id>', methods=['PUT'])
@cross_origin
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
        
        if data['amount']:
            budget.amount = data['amount']
        if data['category']:
            budget.category = data['category']
        if data['description']:
            budget.description = data['description']
        
        budget.date = datetime.datetime.utcnow()

        budget = budget_schema.dump(budget)
        response['data'] = budget
        return response, 201

    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route('/budget/<int:id>', methods=['DELETE'])
@cross_origin
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

        response['data'] = budget.id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route('/budgets', methods=['GET'])
def get_budgets():
    try:
        response = {
            'data':{},
            'error_message':''
        }

        budgets = Budget.query.all()

        budgets = budgets_schema.dump(budgets)
        response['data'] = budgets
        return response, 200

    except Exception as e:
        response['error_message'] = str(e)
        return response, 500