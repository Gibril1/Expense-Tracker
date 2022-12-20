from expense_tracker import db

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(100), nullable =False)

    def __str__(self):
        return self.username

class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(20))
    description = db.Column(db.String(100))
    date = db.Column(db.Date)

    def __str__(self):
        return self.amount

class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(20))

    def __str__(self):
        return self.amount

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    target_amount = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100))

    def __str__(self):
        return self.target_amount





