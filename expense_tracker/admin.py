from expense_tracker import admin, db
from flask_admin.contrib.sqla import ModelView

from expense_tracker.models import (
    Users,
    Savings,
    Budget,
    Expenses,
    Goal
)
class UserModelView(ModelView):
    column_display_pk = True
    column_list = ('username')

class SavingsModelView(ModelView):
    column_display_pk = True
    column_list = (
            'user', 
            'amount', 
            'date_created'
        )

class BudgetModelView(ModelView):
    column_display_pk = True
    column_list = (
            'id',
            'user',
            'start_date',
            'end_date',
            'amount',
            'category'
        )

class ExpensesModelView(ModelView):
    column_display_pk = True
    column_list = (
            'id',
            'user',
            'budget',
            'date',
            'amount',
            'category',
            'description'
    )

class GoalModelView(ModelView):
    column_display_pk = True
    column_list = (
            'id',
            'user',
            'target_amount',
            'target_date',
            'description'
    )
admin.add_view(UserModelView(Users, db.session))
admin.add_view(SavingsModelView(Savings, db.session))
admin.add_view(BudgetModelView(Budget, db.session))
admin.add_view(ExpensesModelView(Expenses, db.session))
admin.add_view(GoalModelView(Goal, db.session))
