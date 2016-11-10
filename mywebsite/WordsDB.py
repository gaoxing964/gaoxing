#-*- coding:utf-8 -*-
__author__ = 'teng.gao'
import json
from Word import Word
import time
from DB import DB


class WordsDB(object):

    def __init__(self ):
        self.connection = DB.getConnection()

    def getWordsByPage(self , firstPage , pageSize  ,field , direction):
        cur = self.connection.cursor()
        firstPage = int(firstPage)
        pageSize = int(pageSize)
        firstIndex = (int(firstPage) - 1)* int(pageSize)
        cur.execute('select wordsId , wordsContent , parentsID , publishTime , raiseflag  from words t where t.parentsID = 0 order by '+field+' '+direction +' limit %s , %s' ,(int(firstIndex ), int(pageSize)))
        results = cur.fetchall()
        words = []
        for word in results:
            wordBean = Word(word)
            words.append(wordBean.getDic())
        cur.execute('select count(wordsId) from words t  where t.parentsID = 0 ')
        count = cur.fetchone()
        return json.dumps({'status':200 , 'data':words , 'totalCount':count})

    def getRaiseWords(self):
        cur = self.connection.cursor()
        cur.execute('select wordsId , wordsContent , parentsID , publishTime , raiseflag  from words t limit 0 , 4 ')
        results = cur.fetchall()
        words = []
        for word in results:
            wordBean = Word(word)
            words.append(wordBean.getDic())
        return json.dumps(words)

    def getSubWords(self , subWOrdsID):
        cur = self.connection.cursor()
        cur.execute('select wordsId , wordsContent , parentsID , publishTime , raiseflag from words t where t.parentsID in ( '+subWOrdsID+' ) ')
        results = cur.fetchall()
        words = []
        for word in results:
            wordBean = Word(word)
            words.append(wordBean.getDic())
        return json.dumps(words)


    def submitWord(self , wordsContent ,parentsID ):
        cur = self.connection.cursor()
        cur.execute('insert into words ( wordsContent , parentsID , publishTime ) values ( %s , %s , %s)',(wordsContent,parentsID,int(time.time())))
        self.connection.commit()
        self.connection.close()
        cur.close()
        return json.dumps({'status':'200','message':'发布成功','data':[]})

