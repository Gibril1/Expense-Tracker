from flask import request
from flask_cors import cross_origin
from expense_tracker import app, db
from expense_tracker.models import Goal
from expense_tracker.serializers import goal_schema, goals_schema
from expense_tracker.auth_middleware import token_required

API_URL = '/api/goals'

@app.route(f'{API_URL}/create', methods=['POST'])
@token_required
def create_goal(f):
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
            user = f.id,
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
def get_goal(f,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goal = Goal.query.get(id)
        if not goal:
            response['error_message'] = f'Goal with {id} id not found'
            return response, 400
        
        if f.id != goal.user:
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
def update_goal(f,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        target_amount= request.json.get('target_amount')
        target_date= request.json.get('target_date')
        description= request.json.get('description')

       

        goal = Goal.query.get(id=id)
        if not goal:
            response['error_message'] = f'Goal with id of {id} not found'
            return response, 400
        
        if f.id != goal.user:
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
def delete_goal(f,id):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goal = Goal.query.get(id)
        if not goal:
            response['error_message'] = f'Goal with {id} id not found'
            return response, 400
        
        if f.id != goal.user:
            response['error_message'] = 'You are not authorised to get this goal'
            return response, 401

        db.session.delete(goal)
        db.session.commit()

        response['data'] = id
        return response, 204
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500

@app.route(f'{API_URL}/', methods=['GET'])
@token_required
def get_goals(f):
    try:
        response = {
            'data':{},
            'error_message':''
        }

        goals = Goal.query.filter_by(user=f.id).all()
        goals = goals_schema.dump(goals)
        response['data'] = goals
        return response, 200
        
    except Exception as e:
        response['error_message'] = str(e)
        return response, 500