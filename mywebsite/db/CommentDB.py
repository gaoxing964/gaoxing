#-*- coding:utf-8 -*-
__author__ = 'teng.gao'
import MySQLdb

class Comment(object):

    def __init__(self , connection):
        self.connection = connection

    def getCommetsByBlogID(self , blogId):
        cur = self.connection.cursor()
        self.connection.select_db('myblog')
        self.connection.select('select t.commentsId , t.commentsContent , t.blogId , t.publishTime  from comments where  t.blogId = %s order by t.publishTime ',[blogId])
        results = cur.fetchall()
        return results


