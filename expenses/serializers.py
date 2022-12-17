from expenses import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'username'
        )

user_schema = UserSchema()