# -*- coding:utf-8 -*-
__author__ = 'teng.gao'


class Blog(object):
    def __init__(self, blog):
        self.blogID = blog[0]
        self.blogTypeID = blog[1]
        self.blogTitle = blog[2]
        self.blogContent = blog[3]
        self.puhlishTime = blog[4]
        self.readCount = blog[5]
        self.raiseFlag = blog[6]
        self.blogKeyWords = blog[7]
        self.blogDescription = blog[8]

    def getDic(self):
        return {'blogID': self.blogID, 'blogTypeID': self.blogTypeID, 'blogTitle': self.blogTitle,
                'blogContent': self.blogContent, 'puhlishTime': self.puhlishTime, 'readCount': self.readCount,'raiseFlag':self.raiseFlag,
                'blogKeyWords': self.blogKeyWords, 'blogDescription': self.blogDescription}
