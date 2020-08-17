"""
序列化

marshmallow 是一个非常优秀的 python 序列化工具，也能欧进行数据校验。 marshmallow 吸收了 django rest framework, flask restful 等优秀框架的思想，api 简单易用，
不和任何平台或框架绑定。 只要是在 python 当中进行序列化或者数据校验，都可以考虑 marshmallow。


## 序列化（Serialization）

序列化是指把编程语言的对象转化成通用的数据，比如把对象转化成二进制流，或者在web 应用中把对象转化成 json 等通用格式,在 marshmallow 中用 dump 进行序列化。

使用 marshmallow 进行序列化：

- 1，编写 Schema ,用于数据转化和校验
- 2，准备需要序列化的对象
- 3，使用 marshmallow.dump 进行序列化


![image.png](https://i.loli.net/2020/08/13/G8INaMBKqEotXwA.png)
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
    

def serial_success():
    schema = UserSchema()
    user1 = User(username='yuz', password='123', age=14)

    # 序列化成功
    user1_serial = schema.dump(user1)
    print(user1_serial)


def serial_failed():
    # 序列化失败
    user2 = User(username='yuz', password='123', age='not a int')
    try:
        user2_serial = schema.dump(user2)
    except Exception as err:
        print(err.args)


def serial_filter_by_only():
    # 通过 only 关键字参数选择需要序列化的字段
    user1 = User(username='yuz', password='123', age=14)
    schema = UserSchema(only=('username', 'age'))
    user_serial_filter = schema.dump(user1)
    print(user_serial_filter)


def serial_filter_by_exclude():
    # 通过 exclude 过滤
    user1 = User(username='yuz', password='123', age=14)
    schema = UserSchema(exclude=('password',))
    user_serial_filter = schema.dump(user1)
    print(user_serial_filter)


def serial_many():
    schema = UserSchema(many=True)
    user1 = User(username='yuz', password='123', age=14)
    user2 = User(username='yuz', password='123', age=15)
    users_serial = schema.dump([user1, user2])
    print(users_serial)

if __name__ == '__main__':
    serial_success()


