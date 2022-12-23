from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
load_dotenv()

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Init app
app = Flask(__name__)

# app config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'models.db')

# Init cors
cors = CORS(app)
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
# Init admin
admin = Admin(app)
# Init bcrypt
bcrypt = Bcrypt(app)
# Init migrate
migrate = Migrate(app, db)


from expense_tracker.routes import (
    user_routes,
    goal_routes,
    budget_routes,
    expenses_routes
)

from expense_tracker.admin import (
    UserModelView,
    SavingsModelView,
    BudgetModelView,
    ExpensesModelView,
    GoalModelView
)


