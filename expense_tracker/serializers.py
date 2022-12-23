from expense_tracker import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'username'
        )

user_schema = UserSchema()


class SavingsSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'user',
            'goal',
            'amount',
            'date_created'
        )

saving_schema = SavingsSchema()
savings_schema = SavingsSchema(many=True)


class ExpensesSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'user',
            'budget',
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
            'user',
            'start_date',
            'end_date',
            'amount',
            'category',
            'status',
            'remainder'
        )

budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)


class GoalSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'user',
            'target_amount',
            'target_date',
            'description'
        )

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)