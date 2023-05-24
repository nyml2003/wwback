from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import date,datetime
from flask.json.provider import DefaultJSONProvider
class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            return super(DefaultJSONProvider, self).default(obj)
        except Exception as e:
            print(obj)
            print(type(obj))
basedir= os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.json = UpdatedJSONProvider(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/Blogdata/instance/tmp.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
CORS(app)
db = SQLAlchemy(app)

blog_lable_table = db.Table('blog_tag',
      db.Column('blog_id', db.Integer, db.ForeignKey('Blog.id'), primary_key=True),
      db.Column('lable_id', db.Integer, db.ForeignKey('Lable.id'), primary_key=True))

blog_pic_table = db.Table('blog_pic',
      db.Column('bloh_id', db.Integer, db.ForeignKey('Blog.id'), primary_key=True),
      db.Column('pic_id', db.Integer, db.ForeignKey('Picture.id'), primary_key=True))

# db.Model是一个基类
class Blog(db.Model):
    # 对应的数据库表明
    __tablename__ ='Blog'
    # 设置字段格式
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('Type.id'),nullable=False)
    #type_name = db.Column(db.String(25),nullable=False)
    description=db.Column(db.String(255),nullable=False)
    title = db.Column(db.String(25),nullable=False)
    content = db.Column(db.Text,nullable=False)
    view = db.Column(db.Integer,default=0)
    like = db.Column(db.Integer,default=0)
    created_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 创建与其他表的关系 
    
    lables = db.relationship('Lable', secondary=blog_lable_table, backref=db.backref('blogs',lazy='dynamic'),lazy='dynamic')
    pictures = db.relationship('Picture', secondary=blog_pic_table, backref=db.backref('blogs',lazy='dynamic'),lazy='dynamic')
    comments=db.relationship('Comment',backref='blog',lazy='dynamic')
    users_like = db.relationship('Like_User_Blog',backref='blog',lazy='dynamic')
    
    #types=db.relationship('Type',backref='blog',lazy='dynamic')
    
    #user=db.relationship('User',backref='blogs',lazy='dynamic')
#    def  __init__(self):
#      self.create_time=datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    def  __repr__(self):
        #return f'blog_id:{self.id},type:{self.type_name},title:{self.title},content:{self.content},view:{self.view},like:{self.like},create_time:{self.create_time},update_time:{self.update_time}'
        return f'blog_id:{self.id},title:{self.title},content:{self.content},view:{self.view},like:{self.like},created_time:{self.created_time},update_time:{self.update_time},discription:{self.discription}'
      

class User(db.Model):
     __tablename__ ='User'
     id = db.Column(db.Integer,primary_key=True)
     user_name = db.Column(db.String(25),nullable=False)
     password = db.Column(db.String(25),nullable=False)
     email = db.Column(db.String(25))
     phone_number = db.Column(db.String(25))
     avatar = db.Column(db.String(255))
     create_time = db.Column(db.DateTime, default=datetime.now)
     
     blogs=db.relationship('Blog',backref='user',lazy='dynamic')
     comments=db.relationship('Comment',backref='user',lazy='dynamic')
     blogs_like = db.relationship('Like_User_Blog',backref='user',lazy='dynamic')
     '''
     def __init__(self,name,password,email=None,phone_number=None):
       self.user_name=name
       self.password=password
       self.email=email
       self.phone=phone_number
     '''
     def  __repr__(self):
        return f'user_id:{self.id},name:{self.user_name},email:{self.email},phone:{self.phone_number},create_time:{self.create_time}'
'''
blog_lable_table = db.Table('blog_tag',
      db.Column('blog_id', db.Integer, db.ForeignKey('Blog.id'), primary_key=True),
      db.Column('lable_id', db.Integer, db.ForeignKey('Lable.id'), primary_key=True))
'''
class Lable(db.Model):
     __tablename__ ='Lable'
     id = db.Column(db.Integer,primary_key=True)
     lable_name = db.Column(db.String(25),nullable=False)
'''     
blog_pic_table = db.Table('blog_pic',
      db.Column('bloh_id', db.Integer, db.ForeignKey('Blog.id'), primary_key=True),
      db.Column('pic_id', db.Integer, db.ForeignKey('Picture.id'), primary_key=True))
'''
class Picture(db.Model):
     __tablename__='Picture'
     id = db.Column(db.Integer,primary_key=True)
     url = db.Column(db.String(255),nullable=False)

class Comment(db.Model):
     __tablename__='Comment'
     id = db.Column(db.Integer,primary_key=True)  
     blog_id = db.Column(db.Integer, db.ForeignKey('Blog.id'),nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
     content = db.Column(db.Text,nullable=False)
     created_time = db.Column(db.DateTime, default=datetime.now)
     
       

class Type(db.Model):
     __tablename__='Type'
     id = db.Column(db.Integer,primary_key=True)  
     type_name = db.Column(db.String(25),nullable=False)
     blogs=db.relationship('Blog',backref='type',lazy='dynamic')

class Like_User_Blog(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
     blog_id = db.Column(db.Integer, db.ForeignKey('Blog.id'),nullable=False)
     like = db.Column(db.Boolean,default=False)
       