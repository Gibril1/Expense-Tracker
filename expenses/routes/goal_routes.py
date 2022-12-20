from flask import request
from flask_cors import cross_origin
from expenses import app, db
from expenses.models import Goal
from expenses.serializers import goal_schema, goals_schema

API_URL = '/api/goals'

@app.route(f'{API_URL}/create', methods=['POST'])
def create_goal():
    try:
        response = {
        'data':{},
        'error_message':''
        }

        # get request body
        data = request.json

        if not data['target_amount'] or not data['target_date']:
            response['error_message'] = 'Please enter all fields'
            return response, 400

        goal = Goal(
            target_amount = data['target_amount'],
            target_date = data['target_date'],
            description = data['description']
        )

        db.session.add(goal)
        db.session.commit()

        goal = goal_schema.dump(goal)
        response['data'] = goal
        return response, 201
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500


@app.route(f'{API_URL}/<int:id>', methods=['GET'])
def get_goal(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goal = Goal.query.get(id=id)
        if not goal:
            response['error_message'] = f'Goal with {id} id not found'
            return response, 400

        goal = goal_schema.dump(goal)
        response['data'] = goal
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['PUT'])
def update_goal(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        data = request.json

        if not data:
            response['error_message'] = 'Data has not been given'
            return response, 400

        goal = Goal.query.get(id=id)
        if not goal:
            response['error_message'] = f'Goal with {id} id not found'
            return response, 400

        if data['target_amount']:
            goal.target_amount = data['target_amount']
        if data['target_date']:
            goal.target_date = data['target_date']
        if data['description']:
            goal.description = data['description']

        goal = goal_schema.dump(goal)
        response['data'] = goal
        return response, 200
        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['DELETE'])
def delete_goal(id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goal = Goal.query.get(id=id)
        if not goal:
            response['error_message'] = f'Goal with {id} id not found'
            return response, 400
        
        db.session.delete(goal)
        db.session.commit()

        response['data'] = id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500
