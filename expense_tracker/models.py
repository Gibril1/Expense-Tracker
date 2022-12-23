from expense_tracker import db, admin



class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(100), nullable =False)

    # linkages
    user_expenses = db.relationship('Expenses', backref='expenses', lazy = True)
    user_budget = db.relationship('Budget', backref='budget', lazy = True)
    user_goals = db.relationship('Goal', backref='goals', lazy = True)
    user_savings = db.relationship('Savings', backref='goals', lazy = True)



    def __str__(self):
        return self.username

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    goal = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = False)
    amount = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    

    def __str__(self):
        return self.amount



class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(20))
    remainder = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean) # if true, the budget has been exceeded else false

    expense_budget = db.relationship('Expenses', backref='expense_budget', lazy=True)

    def __str__(self):
        return self.amount


class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    budget = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(20))
    description = db.Column(db.String(100))
    date = db.Column(db.Date)

    def __str__(self):
        return self.amount



class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    target_amount = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100))
    savings_amount = db.Column(db.Integer, default=0)
    savings = db.relationship('Savings', backref='expense_budget', lazy=True)

    



    def __str__(self):
        return self.target_amount






