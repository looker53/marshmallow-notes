"""
flask-marshmallow 的基础用法和 marshmallow 没什么区别。

只是可以在初始化 app 之后初始化 ma 对象, 其他的用法都一样：
    ma = Marshmallow(app)

重点是和 flask-sqlalchemy 结合。
"""

from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import post_load

app = Flask(__name__)
app.config["SQLALCHEMY_"]
ma = Marshmallow(app)


class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age

    def __repr__(self):
        return f"User<username={self.username}>"


class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "password", "age")

    @post_load
    def to_obj(self, data, **kwargs):
        return User(**data)



@app.route('/serial/')
def serial():
    schema = UserSchema()
    user_obj = User('yuz', '123', 16)
    serialed_user = schema.dump(user_obj)
    return serialed_user


@app.route('/deserial/')
def deserial():
    schema = UserSchema()
    user = {"username": "yuz", "password": "123", "age": 17}
    user_obj = schema.load(user)
    print(user_obj)
    return {"msg": "success"}


if __name__ == '__main__':
    app.run(debug=True)

