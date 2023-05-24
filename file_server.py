from flask import request, jsonify,redirect,url_for
from app import Blog,db,app,User,Type,Comment,Like_User_Blog
from gevent import pywsgi
from datetime import datetime 
import re #用来检测邮件地址是否合法



#获取所有博文，完成情况：已完成
@app.route('/api/SAB',methods=['GET'])
def Select_All_Blogs():
    result=db.session.query(Blog).join(User).join(Type).with_entities(Blog.id, User.user_name, Blog.title,Blog.created_time,Blog.description,User.avatar).all()
    result_list = [dict(zip(['id', 'user_name', 'title','created_time','description','avatar'], row)) for row in result]
    return jsonify(result_list)
#根据博文id获取博文，完成情况：已完成
@app.route('/api/SB',methods=['POST'])
def Select_Blog():
    blog_id=int(request.get_json()['blog_id'])
    blog_raw=db.session.query(Blog).join(User).join(Type).filter(Blog.id == blog_id).with_entities(Blog.id, User.user_name, Type.type_name, Blog.title,Blog.content,Blog.view,Blog.like,Blog.created_time,Blog.description,User.avatar).all()
    blog = [dict(zip(['id', 'user_name', 'type_name', 'title','content','view','like','created_time','description','avatar'], row)) for row in blog_raw][0]
    comments=[]
    for i in db.session.get(Blog,blog_id).comments.all():
        user=db.session.get(User,i.user_id)
        print(i)
        print(i.created_time)
        comments.append({"content":i.content,"user_name":user.user_name,"avatar":user.avatar,"created_time":i.created_time})
    user_id=request.get_json()['user_id']
    like_user_blog=db.session.query(Like_User_Blog).filter_by(user_id=user_id, blog_id=blog_id).first()
    print(like_user_blog)
    blog['isActive']=like_user_blog.like if like_user_blog else False
    blog['comments']=comments
    blog["view"]=blog["view"]+1
    db.session.query(Blog).filter(Blog.id == blog_id).update({'view':Blog.view+1})
    db.session.commit()
    return jsonify(blog)
#登录判断，完成情况：已完成
@app.route('/api/Login_Judge',methods=['GET','POST'])
def login():
  if request.method == 'POST':
    # 获取 JSON 数据
    data = request.get_json()
    user_name = data['name']
    password = data['password']

  # 查询数据库
    user = db.session.query(User).filter_by(user_name=user_name, password=password).first()

    if user:
      # 用户名和密码匹配
      # 在这里执行您想要的操作
      isRight=True
      return jsonify({
          'isRight':isRight,
          'user':{
              'id':user.id,
              'user_name':user_name,
              'avatar':user.avatar,
          }
    })
    else:
      # 用户名和密码不匹配
      # 在这里执行您想要的操作
      isRight=False
      return jsonify({'isRight':isRight,'user':None})

#按标题搜索 完成情况：已完成
@app.route('/api/SCB',methods=['GET','POST'])
def search_blog_by_title():
    title=request.get_json()['title']
    result=db.session.query(Blog).join(User).join(Type).filter(Blog.title.like(f'%{title}%')).with_entities(Blog.id, User.user_name, Blog.title,Blog.created_time,Blog.description,User.avatar).all()
    result_list = [dict(zip(['id', 'user_name', 'title','created_time','description','avatar'], row)) for row in result]
    return jsonify(result_list)
#注册判断，完成情况：已完成
@app.route('/api/Register_Judge',methods=['POST'])
def register():
    # 获取 JSON 数据
    data = request.get_json()
    user_name = data['user_name']
    email = data['email']
    password = data['password']
    #confirmed_password = data['confirmed_password']

    # 创建用户对象并插入到数据库中
    user = User(user_name=user_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    user=db.session.query(User).filter_by(user_name=user_name, email=email, password=password).first()
    return jsonify({
        'id':user.id,
        'user_name':user_name
      })

#插入评论，完成情况：已完成
@app.route('/api/IC',methods=['POST'])
def insertComment():
    data = request.get_json()
    user_id = data['user_id']
    blog_id = data['blog_id']
    content = data['content']
    #lables = data['lables']
    new_comment = Comment(user_id=user_id, blog_id=blog_id, content=content, created_time=datetime.now())
    db.session.add(new_comment)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'status':'Error: {}'.format(str(e))})
    return jsonify({'status':'success'})
    
      
#更新评论，完成情况：未完成
@app.route('/api/UC',methods=['POST'])
def updateComment():
  data = request.get_json()
  user_id = data['user_id']
  blog_id = data['blog_id']
  new_content = data['content']
  comment = Comment.query.filter_by(user_id=user_id, blog_id=blog_id).first()
  if comment:
        comment.content = new_content
        db.session.add(comment)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 'Error: {}'.format(str(e))
        return jsonify({'status':'Comment updated successfully'})
  else:
        return jsonify({'status':'success'})
    

#插入博文 完成情况：已完成
@app.route('/api/IB',methods=['POST'])
def insertBlog():
  data = request.get_json()
  type_id=db.session.query(Type).filter_by(type_name=data['type_name']).first().id
  new_blog = Blog(user_id=data['user_id'], type_id=type_id, description=data['description'], title=data['title'], content=data['content'], created_time=datetime.now(), update_time=datetime.now())
  db.session.add(new_blog)
  try:
        db.session.commit()
  except Exception as e:
        db.session.rollback()
        return jsonify({'Error: {}'.format(str(e))})
  return jsonify({'status':'Blog created successfully'})
  '''
  type1=Type(id=1,type_name='原创')
  type2=Type(id=2,type_name='转载')
  type3=Type(id=3,type_name='翻译')
  '''
  
#更新博文，完成
@app.route('/api/UBC',methods=['GET','POST'])
def updateBlogContent():
  data = request.get_json()
  blog_id = data['blog_id']
  user_id = data['user_id']
  new_content=data['content']
  blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()
  if blog:
        Blog.query.filter_by(id=blog_id, user_id=user_id).update({'content':new_content,'update_time':datetime.now()})
        return jsonify({'status':'Blog updated successfully'})
  else:
        return jsonify({'status':'Blog not found'})
  
@app.route('/api/UBType',methods=['GET','POST'])
def updateBlogType():
  data = request.get_json()
  blog_id = data['blog_id']
  user_id = data['user_id']
  new_type=data['type_name']
  new_type_id=Type.query.filter_by(type_name=new_type).first().id
  blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()
  if blog:
        Blog.query.filter_by(id=blog_id, user_id=user_id).update({'type_id':new_type_id,'update_time':datetime.now()})
        return jsonify({'status':'Blog updated successfully'})
  else:
        return jsonify({'status':'Blog not found'})
  
@app.route('/api/UBTitle',methods=['GET','POST'])
def updateBlogTitle():
  data = request.get_json()
  blog_id = data['blog_id']
  user_id = data['user_id']
  new_title=data['title']
  blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()
  if blog:
        Blog.query.filter_by(id=blog_id, user_id=user_id).update({'title':new_title,'update_time':datetime.now()})
        return jsonify({'status':'Blog updated successfully'})
  else:
        return jsonify({'status':'Blog not found'})
@app.route('/api/UBD',methods=['GET','POST'])
def updateBlogDescription():
  data = request.get_json()
  blog_id = data['blog_id']
  user_id = data['user_id']
  new_description=data['description']
  blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()
  if blog:
        Blog.query.filter_by(id=blog_id, user_id=user_id).update({'description':new_description,'update_time':datetime.now()})
        return jsonify({'status':'Blog updated successfully'})
  else:
        return jsonify({'status':'Blog not found'})
#用户头像更新    
@app.route('/api/UA',methods=['GET','POST'])
def update_avatar():
    user_id=request.get_json()['user_id']
    db.session.query(User).filter(User.id == user_id).update({'avatar':request.get_json()['avatar']})
    return jsonify({'status':'success'})

@app.route('/api/UP',methods=['POST'])
def update_phone():
    user_id=request.get_json()['user_id']
    db.session.query(User).filter(User.id == user_id).update({'phone_number':request.get_json()['phone_number']})
    return jsonify({'status':'success'})
@app.route('/api/UE',methods=['POST'])
def update_email():
    user_id=request.get_json()['user_id']
    db.session.query(User).filter(User.id == user_id).update({'email':request.get_json()['email']})
    return jsonify({'status':'success'})
@app.route('/api/UN',methods=['POST'])
def update_name():
    user_id=request.get_json()['user_id']
    db.session.query(User).filter(User.id == user_id).update({'user_name':request.get_json()['user_name']})
    return jsonify({'status':'success'})
#更新点赞
@app.route('/api/UL',methods=['POST'])
def update_like():
  data = request.get_json()
  blog_id = data['blog_id']
  user_id = data['user_id']
  user_like = data['user_like']#True表明点赞，False表明取消点赞
  print(user_id)
  like_user_blog = db.session.query(Like_User_Blog).filter_by(user_id=user_id, blog_id=blog_id).first()
  #先建立对象
  if not like_user_blog:
    like_user_blog = Like_User_Blog(user_id=user_id, blog_id=blog_id,like=user_like)
    db.session.add(like_user_blog)
  if user_like:
    db.session.query(Blog).filter(Blog.id == blog_id).update({'like':Blog.like+1})
    db.session.query(Like_User_Blog).filter_by(user_id=user_id, blog_id=blog_id).update({'like':True})
  else:
    db.session.query(Blog).filter(Blog.id == blog_id).update({'like':Blog.like-1})
    db.session.query(Like_User_Blog).filter_by(user_id=user_id, blog_id=blog_id).update({'like':False})
  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({'status':'Error: {}'.format(str(e))})
  return jsonify({'status':'Like updated successfully'})

#查询用户信息
@app.route('/api/SP',methods=['GET','POST'])
def select_profile():
  data = request.get_json()
  print(data)
  user_id = data['user_id']
  print(user_id)
  user = db.session.get(User,user_id)
  if user:
        blogs_number = Blog.query.filter_by(user_id=user_id).count()
        likes_number = db.session.query(db.func.sum(Blog.like)).filter(Blog.user_id == user_id).scalar()
        comments_number = Comment.query.filter_by(user_id=user_id).count()
        views_number = db.session.query(db.func.sum(Blog.view)).filter(Blog.user_id == user_id).scalar()
        return jsonify({
            'blogs_number': blogs_number,
            'likes_number': likes_number,
            'comments_number': comments_number,
            'views_number': views_number,
            'id': user.id,
            'email': user.email,
            'phone_number': user.phone_number,
            'created_time': user.create_time
        })
  else:
      return jsonify({'status':'User not found'})

@app.route('/api/DB',methods=['GET','POST'])
def delete_blog():
    data = request.get_json()
    user_id = data['user_id']
    blog_id = data['blog_id']
    blog = Blog.query.filter_by(id=blog_id, user_id=user_id).first()
    if not blog:
        return jsonify({'status': 'Error: Blog not found or not owned by user'})
    Like_User_Blog.query.filter_by(blog_id=blog_id).delete()
    Comment.query.filter_by(blog_id=blog_id).delete()
    db.session.delete(blog)
    try:
        db.session.commit()
        return jsonify({'status': 'Blog deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)})
#根据用户id查询所有博文（不包含评论
@app.route('/api/SMB', methods=['GET','POST'])
def search_my_blogs():
     user_id=request.get_json()['user_id']
     print(user_id)
     blog_raw=db.session.query(Blog).join(User).join(Type).filter(User.id == user_id).with_entities(Blog.id, User.user_name, Blog.title,Blog.created_time,Blog.description,User.avatar).all()
     blog = [dict(zip(['id', 'user_name', 'title','created_time','description','avatar'], row)) for row in blog_raw]
     return jsonify(blog)
   
with app.app_context():
  server = pywsgi.WSGIServer(('0.0.0.0',8180),app)
  server.serve_forever()