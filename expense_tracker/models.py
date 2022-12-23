from expense_tracker import db

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable=False, unique = True, name='username')
    password = db.Column(db.String(100), nullable =False, name='password')

    # linkages
    user_expenses = db.relationship('Expenses', backref='expenses', lazy = True)
    user_budget = db.relationship('Budget', backref='budget', lazy = True)
    user_goals = db.relationship('Goal', backref='goals', lazy = True)
    user_savings = db.relationship('Savings', backref='goals', lazy = True)

    def __str__(self):
        return self.username

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, name='savings_user')
    goal = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = False, name='savings_goal')
    amount = db.Column(db.Integer, nullable=False, name='savings_amount')
    date_created = db.Column(db.Date, nullable=False, name='savings_date')

    def __str__(self):
        return self.amount

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, name='goal_user')
    target_amount = db.Column(db.Integer, nullable=False, name='goal_target_amount')
    target_date = db.Column(db.Date, nullable=False, name='goal_target_date')
    description = db.Column(db.String(100), name='goal_description')
    saved_amount = db.Column(db.Integer, default=0, name='saved_amount_to_goal')

    savings = db.relationship('Savings', backref='expense_budget', lazy=True)

    def __str__(self):
        return self.target_amount


class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, name='budget_user')
    start_date = db.Column(db.Date, nullable=False, name='budget_start_date')
    end_date = db.Column(db.Date, nullable=False, name='budget_end_date')
    amount = db.Column(db.Integer, nullable=False, name='budget_amount')
    category = db.Column(db.String(20), name='budget_category')
    remainder = db.Column(db.Integer, default=0, name='budget_remainder')
    status = db.Column(db.Boolean, name='budget_status') # if true, the budget has been exceeded else false

    expense_budget = db.relationship('Expenses', backref='expense_budget', lazy=True)

    def __str__(self):
        return self.amount


class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, name='expenses_user')
    budget = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable = False, name='expenses_budget')
    amount = db.Column(db.Float, nullable = False, name='amount_spent')
    category = db.Column(db.String(20), name='expenses_category' )
    description = db.Column(db.String(100), name='expenses_description')
    date = db.Column(db.Date,name='expenses_date')

    def __str__(self):
        return self.amount









