from marshmallow import post_load, schema, ValidationError, fields, validate


class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age

    def __repr__(self):
        return f"User<username={self.username}>"


class UserSchema(schema.Schema):
    username = fields.Str(validate=[validate.Length(max=64)])
    password = fields.Str(validate=[validate.Regexp(r"/^(?=.*[a-zA-Z])[\s\S]{8,32}$/")])
    age = fields.Int(validate=[validate.Range(min=6, max=200)])
    gender = fields.Str(validate=[validate.OneOf(['男', '女', '未知'])])


schema = UserSchema()
user = {"username": "hey", "password": "123", "age": 5, "gender": "invalid option"}

# 序列化会正常，
serial = schema.dump(user)
print(serial)

# 反序列化失败
obj = schema.load(user)
print(obj)