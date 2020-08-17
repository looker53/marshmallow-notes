from marshmallow import post_load, schema, ValidationError, fields, validate, validates


class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age

    def __repr__(self):
        return f"User<username={self.username}>"


def in_list(value):
    allowed_data = ['yuz', 'demo']
    if value not in allowed_data:
        raise ValidationError('不是指定的用户')


class UserSchema(schema.Schema):
    username = fields.Str(validate=[in_list, validate.Length(max=2)])
    password = fields.Str(validate=[validate.Regexp(r"/^(?=.*[a-zA-Z])[\s\S]{8,32}$/")])
    age = fields.Int(validate=[validate.Range(min=6, max=200)])
    gender = fields.Str(validate=[validate.OneOf(['男', '女', '未知'])])

    # validates 参数为需要校验的字段
    @validates('username')
    def validate_username_in_list(self, value):
        allowed_data = ['yuz', 'demo']
        if value not in allowed_data:
            raise ValidationError('又不是指定用户')

    @validates('username')
    def validate_username_length_limit(self, value):
        if len(value) < 2:
            raise ValidationError('数据少于 2 个字符')


schema = UserSchema()
user = {"username": "hey"}

# 反序列化失败
obj = schema.load(user)
print(obj)