from marshmallow import post_load, schema, ValidationError, fields


class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age

    def __repr__(self):
        return f"User<username={self.username}>"


class UserSchema(schema.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    age = fields.Int(required=True)
    
    @post_load
    def load_to_orm(self, value, **kwargs):
        return User(**value)

if __name__ == '__main__':
    user_from_dict = {"username": "yuz", "password": "123"}
    schema = UserSchema()
    user = schema.load(user_from_dict)
    print(user)  # 报 ValidationError 错误