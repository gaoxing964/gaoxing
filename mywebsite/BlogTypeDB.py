#-*- coding:utf-8 -*-
__author__ = 'teng.gao'
from BlogType import BlogType
import json
from DB import DB


class BlogTypeDB(object):

    def __init__(self):
        self.connection = DB.getConnection()

    def getAllBlogTypes(self , flag):
        cur = self.connection.cursor()
        cur.execute('select blogTypeID , blogTypeTitle from blogtype ')
        results = cur.fetchall()
        blogTypes = []
        for blogType in results:
            blogTypeBean = BlogType(blogType)
            blogTypes.append(blogTypeBean.getDic())
        if flag == 'template':
            return blogTypes
        else:
            return json.dumps(blogTypes)




