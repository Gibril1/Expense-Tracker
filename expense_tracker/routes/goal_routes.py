from flask import request
from flask_cors import cross_origin
from expense_tracker import app, db
from expense_tracker.models import Goal, Budget
from expense_tracker.serializers import goal_schema, goals_schema
from expense_tracker.auth_middleware import token_required

API_URL = '/api/goals'

@app.route(f'{API_URL}/create/<int:id>', methods=['POST'])
@token_required
def create_goal(user, id):
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
        
        # get the specific budget in which this expense is being deducted from
        budget = Budget.query.get(id)

        if not budget:
            response['error_message'] = f'Budget with id of {id} does not exist'
            return response, 400


        goal = Goal(
            target_amount = data['target_amount'],
            user = user.id,
            budget = budget.id,
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
@token_required
def get_goal(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goal = Goal.query.get(id)
        if not goal:
            response['error_message'] = f'Goal with {id} id not found'
            return response, 400
        
        if user.id != goal.user:
            response['error_message'] = 'You are not authorised to get this goal'
            return response, 401

        goal = goal_schema.dump(goal)
        response['data'] = goal
        return response, 200
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['PUT'])
@token_required
def update_goal(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        target_amount= request.json.get('target_amount')
        target_date= request.json.get('target_date')
        description= request.json.get('description')

       

        goal = Goal.query.get(id)
        if not goal:
            response['error_message'] = f'Goal with id of {id} not found'
            return response, 400
        
        if user.id != goal.user:
            response['error_message'] = 'You are not authorised to get this goal'
            return response, 401

        if target_amount:
            goal.target_amount = target_amount
        if target_date:
            goal.target_date = target_date
        if description:
            goal.description = description

        goal = goal_schema.dump(goal)
        response['data'] = goal
        return response, 200
        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/<int:id>', methods=['DELETE'])
@token_required
def delete_goal(user,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goal = Goal.query.get(id)
        if not goal:
            response['error_message'] = f'Goal with {id} id not found'
            return response, 400
        
        if user.id != goal.user:
            response['error_message'] = 'You are not authorised to get this goal'
            return response, 401

        db.session.delete(goal)
        db.session.commit()

        response['data'] = id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/all/<int:id>', methods=['GET'])
@token_required
def get_goals(user, id):
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

        goals = Goal.query.filter_by(budget=budget.id).all()
        goals = goals_schema.dump(goals)
        response['data'] = goals
        return response, 200
        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500