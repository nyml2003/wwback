from app import app,db,User,Blog,Lable,Comment,Type

with app.app_context():
  db.drop_all()
  db.create_all()
  #User数据
  user1=User(user_name='user1',password='12345',avatar="https://img-blog.csdnimg.cn/3f2168d4130c442d80b50d4b07852667.jpeg#pic_center",email="thisisemail@test.com",phone_number="123456")
  user2=User(user_name='user2',password='54321',avatar="https://img2.baidu.com/it/u=347016863,223465354&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500",email="thatisemail@test.com",phone_number="654321")
  user3=User(user_name='admin',password="admin",avatar="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F202005%2F03%2F20200503102008_rnyye.thumb.1000_0.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1687178804&t=4134d1959be723828702744f64fbeb8f",email="admin@test",phone_number="123456789")
  db.session.add_all([user1,user2,user3])
  db.session.commit()
  #Lable数据
  lable1=Lable(lable_name='math')
  lable2=Lable(lable_name='study')
  lable3=Lable(lable_name='chinese')
  db.session.add_all([lable1,lable2,lable3])
  db.session.commit()
  #BLOG,type数据
  type1=Type(id=1,type_name='原创')
  type2=Type(id=2,type_name='转载')
  type3=Type(id=3,type_name='翻译')
  db.session.add_all([type1,type2,type3])
  blog1=Blog(
    user_id=user1.id,
    title='深度学习架构的对比分析',
    content='''
**PART**  **01 MAC&IP的自白**

**MAC地址说：**

我是MAC地址，工作在**数据链路层**，生活在**物理网卡**上。

![img](https://img-blog.csdnimg.cn/img_convert/d2648fcdca7ab6e82789f96e3d8e341c.png)

我对感情非常专一，从不朝三暮四，这一辈子我的“CP”都是同一块网卡。我们的感情非常稳定，**每一块网卡都只有一个独一无二的MAC地址**，不像IP地址那样见异思迁。

**IP地址说：**

我是IP地址，工作在**网络层**，生活在**IP协议簇**中。

![img](https://img-blog.csdnimg.cn/img_convert/b6758b3f7c76191ef23cdd416a1400e7.png)

有人说我是“万花丛中过，片叶不沾身”，经常和不同的设备“组CP”，特别是MAC地址，经常说我见异思迁。

但其实生活不易，**我在同一时间也只有唯一的一个“CP”**，和这个设备的CP组合到期了，我还没来得及休息一下下，就被安排去和另外一个设备“组CP”了。

停停停！你俩是不是偏题了！

**还是让文档君来正经介绍吧！**

**PART** **02 MAC地址是啥**？

**MAC地址**，全称为**Media Access Control Address**，直译为**媒体存取控制地址**，又名物理地址、硬件地址。 每个网卡出厂时，厂家都会为其标记全球独一无二的序列号，就像我们的**身份证号**。

**PART** **03**  **IP地址是啥？**

**IP地址**，全称为**Internet Protocol Address**，直译为**互联网协议地址**。

主要用来在互联网中区分不同的联网设备。

IP地址为连入互联网（公网）内的每台设备提供一个独一无二的逻辑地址标识。通过IP地址，我们可以在互联网中准确找到目标设备，并与其建立通信。就像现实生活中网购时填写的**收件地址**。

IP地址与MAC地址不同的是，为保证网络高效运行，**IP地址是动态分配的**，也可以人为修改，就好比你可以到处搬家，或者可以去“有风的地方”看一看~

**但是MAC地址不可以随意改变**，就像你的身份证号，无论你搬到哪里，身份证号都是证明“你是你”的最有效的凭证~

**PART** **04 IP&MAC区别？**

其实MAC地址和IP地址有很多不同，文档君整理了MAC地址和IP地址的区别，让你一眼看懂~

![在这里插入图片描述](https://img-blog.csdnimg.cn/78f79703cc4c40afb199a0657b696ad9.png)

**PART** **05 为何缺一不可**？

简单来说，IP地址和MAC地址产生的目的是方便网络中的设备精准地找到彼此。

沿用前文的例子，我们把MAC地址比作身份证号码，把IP地址比作住址。

如果只有身份证号码（MAC地址），在茫茫人海中肯定找不到你心爱的文档君。

如果只有住址（IP地址），你找到了文档君的家，但是家里具体哪个人是文档君呢？还是无法分清。

但是如果把住址（IP地址）和身份证号（MAC地址）配合使用，就可以先找到省→市→区→街道→小区，再通过身份证号码（MAC地址）就可以很容易地抓到在屏幕前码字的文档君啦。

**同理，设备在进行通信的时候，IP地址和MAC地址也是缺一不可。**

在网络上，通信的双方在同一局域网（LAN）内的情况是很少的，通常是经过多台计算机和网络设备中转才能连接到对方。因为IP地址在一个LAN中是唯一的，但是在不同的局域网中，IP地址可能是相同的，而且IP地址可以手动更改，这就可能导致重复的IP地址。但MAC地址是唯一的，不同的设备上的MAC地址是完全不同的，所以不同的局域网依靠MAC地址来识别不同的设备，从而避免IP地址的冲突。
![img](https://img-blog.csdnimg.cn/img_convert/76a06deebf67c35b76a8f24d3cd8961a.png)

因此，**“IP地址+MAC地址”才是真正的“CP”**，他俩配合使用才能确定网络中唯一的一台设备，数据传输才不会出错。

    ''',
    type_id=type2.id,
    description='深度学习的概念源于人工神经网络的研究，含有多个隐藏层的多层感知器是一种深度学习结构。深度学习通过组合低层特征形成更加抽象的高层表示，以表征数据的类别或特征。它能够发现数据的分布式特征表示。深度学习是机器学习的一种，而机器学习是实现人工智能的必经之路'
  )
  
  db.session.add_all([blog1])
  db.session.commit()

  comment1=Comment(blog_id=blog1.id,user_id=user1.id,content='nice')
  comment2=Comment(blog_id=blog1.id,user_id=user2.id,content='good text')
  comment3=Comment(blog_id=blog1.id,user_id=user3.id,content='user2 say something')
  db.session.add_all([comment1,comment2,comment3])
  db.session.commit()
  