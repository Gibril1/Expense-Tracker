from expenses import db

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(100), nullable =False)

class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(20))
    description = db.Column(db.String(100))
    date = db.Column(db.Datetime)

    def __str__(self):
        return self.amount
