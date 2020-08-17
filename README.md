marshmallow 的学习笔记代码, 代码在 demo 文件。

主要包含：
- 基础使用
- 序列化
- 序列化数据删选过滤
- 反序列化
- 反序列化数据校验
- required 参数
- 内置校验器
- 自定义校验器
- flask-marshmallow



marshmallow 是一个非常优秀的 python 序列化工具，也能欧进行数据校验。 marshmallow 吸收了 django rest framework, flask restful 等优秀框架的思想，api 简单易用，
不和任何平台或框架绑定。 只要是在 python 当中进行序列化或者数据校验，都可以考虑 marshmallow。


## 序列化（Serialization）

序列化是指把编程语言的对象转化成通用的数据，比如把对象转化成二进制流，或者在web 应用中把对象转化成 json 等通用格式,在 marshmallow 中用 dump 进行序列化。

使用 marshmallow 进行序列化：

- 1，编写 Schema ,用于数据转化和校验
- 2，准备需要序列化的对象
- 3，使用 marshmallow.dump 进行序列化


![image.png](https://i.loli.net/2020/08/13/G8INaMBKqEotXwA.png)


```python
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
    
    
schema = UserSchema()
user1 = User(username='yuz', password='123', age=14)

# 序列化成功
user1_serial = schema.dump(user1)
print(user1_serial)



```

**说明**：

- UserSchema 中的字段名称和 User 的属性名称一致
- fields.Str() 表示字段必须能够转化成字符串。fields.Int() 必须能转化成整型
- 当因为 fields 类型不满足序列化失败的时候，会抛出 ValueError 异常


```python
# 序列化失败
user2 = User(username='yuz', password='123', age='not a int')
user2_serial = schema.dump(user2)
print(user2_serial) # 报错
```

## 序列化失败的异常处理

当序列化失败时，会抛出异常。比如 filed 转化失败会抛出 ValueError 异常。

可以通过捕获异常获取错误原因, err.args 得到错误原因

TODO:(不明白为什么 marshmallow 序列化失败要抛出 ValueError , 而不是统一用 ValidationError)


```python
# 序列化失败
user2 = User(username='yuz', password='123', age='not a int')
try:
    user2_serial = schema.dump(user2)
except Exception as err:
    print(err.args)
```

## 序列化的数据过滤（Filtering）

序列化必须要考虑安全和带宽问题。敏感数据不能暴露的应该过滤，或者混淆加密。还有一些冗余数据没有必要暴露的有要过滤。

比如 User 当中的 password 应该被过滤。

![marshmallow-02-filtering.png](https://i.loli.net/2020/08/13/UmoVzNThDFqrW3b.png)


数据过滤有 2 中形式：

- 通过 only 关键参数选择需要序列化的字段白名单，数据类型是元组或者列表
- 通过 exclude 关键字参数选择需要过滤掉的字段黑名单，数据类型是元组或者列表


```python
# 通过 only 关键字参数选择需要序列化的字段
schema = UserSchema(only=('username', 'age'))
user_serial_filter = schema.dump(user1)
print(user_serial_filter)
```


```python
# 通过 exclude 过滤
schema = UserSchema(exclude=('password',))
user_serial_filter = schema.dump(user1)
print(user_serial_filter)
```

## 序列化多个数据

现在有多个 User 对象需要同时序列化，这在 web 应用当中获取列表信息时总会用到。

多数据序列化可以在 Schema 初始化时传入 many=True 参数，执行 dump 时传入列表就可以了。


```python
schema = UserSchema(many=True)
user1 = User(username='yuz', password='123', age=14)
user2 = User(username='yuz', password='123', age=15)
users_serial = schema.dump([user1, user2])
print(users_serial)
```

user1 和 user2 都序列化成功，如果其中有一个没有通过，则会引发异常。

那有没有一种方法忽略引发异常的单个数据，返回能正常序列化的数据呢？

TODO:(通过阅读源码发现每个字段不符合就会报错，没有对错误进行统一的调度。先在 stackoverflow 和 github 提问)
issue: https://github.com/marshmallow-code/marshmallow/issues/1647


```python
schema = UserSchema(many=True)
user1 = User(username='yuz', password='123', age=14)
user2 = User(username='yuz', password='123', age="not a int")
users_serial = schema.dump([user1, user2])
print(users_serial)
```

## 反序列化（Deserialization）

反序列化是指把通用数据转化成编程语言的对象，比如把二进制流转化成对象，或者在web 应用中把 json 等通用格式转成对象。

![marshmallow-03-load.png](https://i.loli.net/2020/08/13/RlB91Co2zeQ7kmJ.png)

在 marshmallow 中，load 方法默认会对字典进行校验，转化后还是字典,只起到了数据校验的作用。
如果是要对 json 字符串进行校验，可以使用 loads 方法。


```python
# dict to dict
user_from_dict = {"username": "yuz", "password": "123"}
schema = UserSchema()
user = schema.load(user_from_dict)
print(user)

# json string to dict
json_user = '{"username": "yuz", "password": "123"}'
schema = UserSchema()
user = schema.loads(json_user)
print(user)     
```

## 反序列化中没有 Schema 字段

传入的原始数据没有 age 字段，是没有问题的，但是如果有多余的字段而 schema 中没有定义，则不可以。

此时会报 ValidationError 错误


```python
user_from_dict = {"username": "yuz", "password": "123", "gender": "男"}
schema = UserSchema()
user = schema.load(user_from_dict)
print(user)
```

## 反序列化失败

反序列化失败会报 ValidationError错误， 和序列化的 ValueError 不一样。(TODO: Why)

## 反序列化成 ORM 对象

基本上不会去干把字典转化成字典的事，反而是在 web 应用中需要校验用户传输的数据是不是能够转化成数据库的 ORM 模型对象。假设 User 类就是 ORM.

要转化成 ORM 需要做：

- 通过 post_load 声明在调用 load 时的行为。（也可以通过 post_dump 装饰器进行序列化操作）
- 在 Schema 中定义方法，决定转化成什么对象。
- 行为当中传入 value 参数和 `**kwargs`, 注意 `**kwargs` 不能省略



**使用 flask-marshmallow 等集成库使用会更简单**



```python
from marshmallow import post_load, schema


class UserSchema(schema.Schema):
    username = fields.Str()
    password = fields.Str()
    age = fields.Int()
    
    @post_load
    def load_to_orm(self, value, **kwargs):
        return User(**value)
    
    
user_from_dict = {"username": "yuz", "password": "123", "age":14}
schema = UserSchema()
user = schema.load(user_from_dict)
print(user)
    
```

## ORM 中异常处理


```python

from marshmallow import post_load, schema, ValidationError


class UserSchema(schema.Schema):
    username = fields.Str()
    password = fields.Str()
    age = fields.Int()
    
    @post_load
    def load_to_orm(self, value, **kwargs):
        try:
            return User(**value)
        except Exception as e:
#             raise ValidationError(str(e))
            print(f"不能完成对象转化{e}")
    
    
user_from_dict = {"username": "yuz", "password": "123"}
schema = UserSchema()
user = schema.load(user_from_dict)
print(user)

```

## 反序列化的多值处理


```python
user1 = {"username": "yuz", "password": "123", "age": 12}
user2 = {"username": "demo", "password": "456",  "age": 18}
schema = UserSchema(many=True)
user = schema.load([user1, user2])
print(user)

```

## 内置的常用 Field 

- Str
- Int
- Date
- URL
- Email

## Field 常用参数

- required
- validate

## required 参数

表示在进行反序列化中，必须要有相关字段，否则无法转化成对应的对象， 比如在 ORM 转化 load_to_orm 中，由于 age 没有传入会导致 User 对象初始化失败，
所以应该把 schema 当中的字段都设置成 required。当没有传入相关字段时，在初始化 User 之前就会包 ValidatrionError 错误。




```python
from marshmallow import post_load, schema, ValidationError


class UserSchema(schema.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    age = fields.Int(required=True)
    
    @post_load
    def load_to_orm(self, value, **kwargs):
        return User(**value)
    
    
user_from_dict = {"username": "yuz", "password": "123"}
schema = UserSchema()
user = schema.load(user_from_dict)
print(user)  # 报 ValidationError 错误
```

**required 参数在序列化时无效**




```python
class User:
    def __init__(self, username):
        self.username = username
        
user = User("yuz")
schema = UserSchema()
serial_data = schema.dump(user)
print(serial_data)  # 
```

## 内置校验器 Validator

如果对数据字段需要进一步校验，需要用到 field 当中的 validate 参数。

marshmallow 的数据校验写法充分吸收了 django rest framework 和 flask wtform 的写法长处。
注意：数据校验都是针对反序列化 load 操作， 序列化操作是没有数据校验的。

常用的校验器有:

- Length
- Range
- Equal
- OneOf
- URL
- Email
- Regexp


```python
from marshmallow import schema, fields, validate


class UserSchema(schema.Schema):
    username = fields.Str(validate=[validate.Length(max=64)])
    password = fields.Str(validate=[validate.Regexp(r"/^(?=.*[a-zA-Z])[\s\S]{8,32}$/")])
    age = fields.Int(validate=[validate.Range(min=6,max=200)])
    gender = fields.Str(validate=[validate.OneOf(['男', '女', '未知'])])
    
    
schema = UserSchema()
user = {"username": "hey", "password": "123", "age": 5, "gender": "invalid option"}

# 序列化会正常，
serial = schema.dump(user)
print(serial)  

# 反序列化失败
obj = schema.load(user)
print(obj)



```

## 自定义校验器 validator

有时候你需要定制某个字段需要符合的规则，可以自己定义一个函数做为 validator, 接收 value 为参数，当不符合规则是，抛出异常。


```python
from marshmallow import schema, fields, validate, ValidationError


def in_list(value):
    allowed_data = ['yuz', 'demo']
    if value not in allowed_data:
        raise ValidationError('不是指定的用户')


class UserSchema(schema.Schema):
    username = fields.Str(validate=[in_list, validate.Length(max=2)])
    password = fields.Str(validate=[validate.Regexp(r"/^(?=.*[a-zA-Z])[\s\S]{8,32}$/")])
    age = fields.Int(validate=[validate.Range(min=6,max=200)])
    gender = fields.Str(validate=[validate.OneOf(['男', '女', '未知'])])
    
    
schema = UserSchema()
user = {"username": "hey"}


# 反序列化失败
obj = schema.load(user)
print(obj)

```

## 使用装饰器自定义 validator

还有另外的一种方式提供自定义的校验器。

可以在 Schema 下定义一个方法，用 validators 装饰器装饰。

但是这种方式不能为同一个字符设置多个方法校验，只有一个生效。不灵活。


```python
from marshmallow import schema, fields, validate, ValidationError, validates


class UserSchema(schema.Schema):
    username = fields.Str()
    password = fields.Str(validate=[validate.Regexp(r"/^(?=.*[a-zA-Z])[\s\S]{8,32}$/")])
    age = fields.Int(validate=[validate.Range(min=6,max=200)])
    gender = fields.Str(validate=[validate.OneOf(['男', '女', '未知'])])
    
    # validates 参数为需要校验的字段
    @validates('username')
    def validate_username_in_list(self, value):
        allowed_data = ['yuz', 'demo']
        if value not in allowed_data:
            raise ValidationError('又不是指定用户')
            
    @validates('username')
    def validate_username_length_limit(self,value):
        if len(value) < 2:
            raise ValidationError('数据少于 2 个字符')
    
    
schema = UserSchema()
user = {"username": "hey"}


# 反序列化失败
obj = schema.load(user)
print(obj)
```



## flask-marshmallow 的使用

该插件主要对 flask 框架做了一些集成，当使用 orm 的时候可以根据 orm 对象自动生成 Schema 校验字段。



在反序列化时，不会自动转成 orm 对象，可以自己通过 @post_load 装饰器实现。

```python
ma = Marshmallow(app)


class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author

    id = ma.auto_field()
    name = ma.auto_field()
    books = ma.auto_field()


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True
        fields = ()
        
    @post_load
    def to_orm():
        pass

```



- 通常来说，不需要通过 fileds = ("username",) 过滤，而是在初始化的时候提供 only 或者 exclude 参数。

```
schema = BookSchema(only=())
```

- 在反序列化 load 时，需要对数据校验，必须传入的参数可以通过 nullable 参数改变 ORM 对象， 数据校验时是通过 ORM 对象的参数要求校验的。



## Issues

- [#1650](https://github.com/marshmallow-code/marshmallow/issues/1650)

- [#1647](https://github.com/marshmallow-code/marshmallow/issues/1647)