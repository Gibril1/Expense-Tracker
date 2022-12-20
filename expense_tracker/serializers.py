from expense_tracker import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'username'
        )

user_schema = UserSchema()

class ExpensesSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'date',
            'amount',
            'category',
            'description'
        )

expenses_schema = ExpensesSchema()
expensess_schema = ExpensesSchema(many=True)


class BudgetSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'start_date',
            'end_date',
            'amount',
            'category'
        )

budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)


class GoalSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'target_amount',
            'target_date',
            'description'
        )

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)