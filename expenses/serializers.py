from expenses import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'username'
        )

user_schema = UserSchema()

class BudgetSchema(ma.Schema):
    class Meta:
        fields = (
            'date',
            'amount',
            'category',
            'description'
        )

budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)