#-*- coding:utf-8 -*-
__author__ = 'teng.gao'

class BlogType(object):

    def __init__(self , blogType):
        self.blogTypeID = blogType[0]
        self.blogTypeTitle = blogType[1]

    def getDic(self):
        return {'blogTypeID':self.blogTypeID,'blogTypeTitle':self.blogTypeTitle}
