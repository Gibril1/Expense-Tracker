from expenses import ma

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