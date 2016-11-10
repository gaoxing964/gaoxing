# -*- coding:utf-8 -*-
__author__ = 'teng.gao'

import json
from Blog import Blog
from DB import DB
import  time

class BlogDB(object):
    def __init__(self):
        self.connection = DB.getConnection()

    def getBlogByPage(self, firstPage, pageSize , blogTypeID):
        firstIndex = (int(firstPage) - 1) * int(pageSize)
        cur = self.connection.cursor()
        cur.execute( 'select t.blogID , t.blogTypeID , t.blogTitle , t.blogContent , t.puhlishTime  , t.readCount   ,t.raiseFlag, blogKeyWords , blogDescription from blog t where ( %s = 0  or   t.blogTypeID = %s ) limit  %s , %s  ',(int(blogTypeID),int(blogTypeID),int(firstIndex), int(pageSize)))
        results = cur.fetchall()
        blogs = []
        for blog in results:
            blogBean = Blog(blog)
            blogs.append(blogBean.getDic())
        cur.execute('select count(1)  from blog t where ( %s = 0  or   t.blogTypeID = %s )  ' , (int(blogTypeID),int(blogTypeID)))
        count = cur.fetchone()
        return json.dumps({'status': 200, 'data': blogs, 'allCount': count})

    def getNewestBlogs(self , flag):
        cur = self.connection.cursor()

        cur.execute(
            'select t.blogID , t.blogTypeID , t.blogTitle , t.blogContent , t.puhlishTime , t.readCount  ,t.raiseFlag, blogKeyWords , blogDescription  from blog t order by t.puhlishTime desc  limit 0 , 10 ')
        results = cur.fetchall()
        blogs = []
        for blog in results:
            blogBean = Blog(blog)
            blogs.append(blogBean.getDic())
        if flag == 'template' :
            return blogs
        else:
            return json.dumps(blogs)

    def getHotestBlogs(self , flag):
        cur = self.connection.cursor()
        cur.execute('select t.blogID , t.blogTypeID , t.blogTitle , t.blogContent , t.puhlishTime , t.readCount  ,t.raiseFlag, blogKeyWords , blogDescription from blog t order by t.readCount desc limit 0 , 10 ')
        results = cur.fetchall()
        blogs = []
        for blog in results:
            blogBean = Blog(blog)
            blogs.append(blogBean.getDic())
        if flag == 'template' :
            return blogs
        else:
            return json.dumps(blogs)

    def getTopFiveRaiseBlogs(self):
        cur = self.connection.cursor()
        cur.execute(
            'select t.blogID , t.blogTypeID , t.blogTitle , t.blogContent , t.puhlishTime , t.readCount ,t.raiseFlag,   blogKeyWords , blogDescription from blog t  where t.raiseFlag = 1 limit 0 , 5 ')
        results = cur.fetchall()
        blogs = []
        for blog in results:
            blogBean = Blog(blog)
            blogs.append(blogBean.getDic())
        return json.dumps(blogs)

    def submitSingleBlog(self,blog):
		cur = self.connection.cursor()
		cur.execute('insert into blog ( blogTypeID , blogTitle , blogContent , puhlishTime , readcount, raiseFlag , blogKeyWords , blogDescription ) values ( %s , %s , %s , %s , %s  , %s , %s , %s )' , (int(blog.blogTypeID) , blog.blogTitle , blog.blogContent , int(time.time()),0, blog.raiseFlag , blog.blogKeyWords , blog.blogDescription))
		self.connection.commit()
		self.connection.close()
		cur.close()
		return json.dumps({'status':'200','message':'发布成功','data':[]})

    def getSingleBlog(self,blogID):
        cur = self.connection.cursor()
        cur.execute('select t.blogID , t.blogTypeID , t.blogTitle , t.blogContent , t.puhlishTime , t.readCount ,t.raiseFlag, blogKeyWords , blogDescription  from blog t  where t.blogID = %s ',(blogID,))
        result = cur.fetchone()
        blogBean = Blog(result)
        return blogBean.getDic()

    def deleteBlog(self , blogID):
        cur = self.connection.cursor()
        cur.execute('delete from blog   where blogID = %s ',(int(blogID)))
        self.connection.commit()
        self.connection.close()
        cur.close()
        return json.dumps({'status':'200','message':'删除成功','data':[]})

    def modifyBlog(self,blog):
		cur = self.connection.cursor()
		cur.execute('update blog set  blogTypeID = %s , blogTitle = %s , blogContent = %s, puhlishTime = %s , readcount = %s , raiseFlag  = %s , blogKeyWords = %s  , blogDescription = %s  where blog.blogID = %s' , (int(blog.blogTypeID) , blog.blogTitle , blog.blogContent , int(time.time()),0, blog.raiseFlag , blog.blogKeyWords , blog.blogDescription , blog.blogID))
		self.connection.commit()
		self.connection.close()
		cur.close()
		return json.dumps({'status':'200','message':'修改成功','data':[]})

    def hasReadBlog(self,blogID):
        cur = self.connection.cursor()
        cur.execute('update blog set    readcount = readcount + 1   where blog.blogID = %s' , (blogID,))
        self.connection.commit()
        self.connection.close()
        cur.close()
        return json.dumps({'status':'200','message':'修改成功','data':[]})


        



		
