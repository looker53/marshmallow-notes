"""反序列化
"""

from marshmallow import schema, fields


class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age
        
    def __repr__(self):
        return f"User<username={self.username}>"
    
    
class UserSchema(schema.Schema):
    username = fields.Str()
    password = fields.Str()
    age = fields.Int()
    

def deserial():
    user_from_dict = {"username": "yuz", "password": "123"}
    schema = UserSchema()
    user = schema.load(user_from_dict)
    print(user)

if __name__ == '__main__':
    deserial()





