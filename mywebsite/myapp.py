#-*- coding:utf-8 -*-
__author__ = 'teng.gao'

from flask import Flask, request, render_template
import MySQLdb
from datetime import date
from  BlogDB import  BlogDB
from BlogTypeDB import BlogTypeDB
from WordsDB import WordsDB
from Blog import Blog
#import sae
import time
from jinja2 import Environment, FileSystemLoader
from DB import DB
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
env = Environment(loader=FileSystemLoader('/templates'))
def format_date(dateString):
    rightDate = dateString[0:4] + '年'+dateString[4:6]+'月'+dateString[6:8]+'日'
    return rightDate

env.filters['format_date'] = format_date

app = Flask(__name__)

@app.route('/foots', methods=['GET', 'POST'])
def home():
    return render_template('foots.html')

@app.route('/words', methods=['GET'])
def words():
    return render_template('words.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/skatings', methods=['GET'])
def skatings():
    return render_template('skatings.html')

@app.route('/studies', methods=['GET'])
def studies():
    return render_template('studies.html')
    
@app.route('/toWriteBlog', methods=['GET'])
def toWriteBlog():
    return render_template('submitBlog.html', operationType="ADD" )

@app.route('/toManageBlog', methods=['GET'])
def toManageBlog():
    return render_template('manage.html')

@app.route('/singleBlog/<int:blogID>', methods=['GET'])
def singleBlog(blogID):
    blogDB = BlogDB()
    blog = blogDB.getSingleBlog(blogID)
    hotestBlogs = blogDB.getHotestBlogs('template')
    newstBlogs = blogDB.getNewestBlogs('template')
    blogTypeDB = BlogTypeDB()
    blogTypes = blogTypeDB.getAllBlogTypes('template')
    blogDB.hasReadBlog(blogID)
    return render_template('singleBlog.html',blog = blog , hotestBlogs = hotestBlogs , newstBlogs = newstBlogs ,blogTypes = blogTypes )

@app.route('/getSingleBlog/<blogID>', methods=['GET'])
def getSingleBlog(blogID):
    blogdb = BlogDB()
    return blogdb.getSingleBlog(blogID)

@app.route('/api/getNewstBlogs',methods=['GET'])
def getNewstBlogs():
    blogdb = BlogDB()
    return blogdb.getNewestBlogs('ajax')

@app.route('/api/getHotestBlogs',methods=['GET'])
def getHotestBlogs():
    blogdb = BlogDB()
    return blogdb.getHotestBlogs('ajax')

@app.route('/api/getTopFiveRaiseBlogs',methods=['GET'])
def getTopFiveRaiseBlogs():
    blogdb = BlogDB()
    return blogdb.getTopFiveRaiseBlogs()

@app.route('/api/blogType/getAllBlogTypes',methods=['GET'])
def getAllBlogTypes():

    blogTypeDB = BlogTypeDB()
    return blogTypeDB.getAllBlogTypes('ajax')

@app.route('/api/getBlogByPage',methods=['POST'])
def getBlogByPage():
    currentPage = request.form['currentPage']
    pageSize = request.form['pageSize']
    blogTypeID = request.form['blogTypeID']
    if blogTypeID is None :
        blogTypeID = 0

    blogDb = BlogDB()
    return blogDb.getBlogByPage(currentPage,pageSize,blogTypeID)

@app.route('/api/getRaiseWords',methods=['GET'])
def getRaiseWords():

    wordDB = WordsDB()
    return wordDB.getRaiseWords()

@app.route('/api/getWordsByPage/<currentPage>/<pageSize>/<somefield>/<direction>',methods=['GET'])
def getWordsByPage(currentPage,pageSize , somefield , direction):

    wordDB = WordsDB()
    return wordDB.getWordsByPage(currentPage ,pageSize , somefield , direction )

@app.route('/api/getSubWords/<subWOrdsID>',methods=['GET'])
def getSubWords(subWOrdsID):

    wordDB = WordsDB()
    return wordDB.getSubWords(subWOrdsID )

@app.route('/api/submitWord/<wordsContent>/<parentsID>',methods=['GET'])
def submitWord(wordsContent ,parentsID ):

    wordDB = WordsDB()
    return wordDB.submitWord(wordsContent ,parentsID  )

@app.route('/api/deleteBlog/<blogID>',methods=['GET'])
def deleteBlog(blogID):
    blogDb = BlogDB()
    return blogDb.deleteBlog(blogID)

@app.route('/showBlog',methods=['GET'])
def showBlog():
    blogDB = BlogDB()
    hotestBlogs = blogDB.getHotestBlogs('template')
    newstBlogs = blogDB.getNewestBlogs('template')
    blogTypeDB = BlogTypeDB()
    blogTypes = blogTypeDB.getAllBlogTypes('template')
    return render_template('show.html', hotestBlogs = hotestBlogs , newstBlogs = newstBlogs ,blogTypes = blogTypes )


@app.route('/api/modifyBlog',methods=['POST'])
def modifyBlog():
    blogdb = BlogDB()
    blogID = request.form['blogID'];
    blogTitle = request.form['blogTitle']
    blogContent = request.form['blogContent']
    blogTypeID = request.form['blogTypeID']
    raiseFlag = request.form['raiseFlag']
    blogKeyWords = request.form['blogKeyWords']
    blogDescription = request.form['blogDescription']
    blog = Blog([blogID,blogTypeID,blogTitle , blogContent ,int(time.time()) ,0,0,blogKeyWords , blogDescription])
    return blogdb.modifyBlog(blog)



    
@app.route('/submitBlog', methods=['POST'])
def submitBlog():

    blogdb = BlogDB()
    blogTitle = request.form['blogTitle']
    blogContent = request.form['blogContent']
    blogTypeID = request.form['blogTypeID']
    raiseFlag = request.form['raiseFlag']
    blogKeyWords = request.form['blogKeyWords']
    blogDescription = request.form['blogDescription']
    blog = Blog([1,blogTypeID,blogTitle , blogContent ,int(time.time()) ,0,0,blogKeyWords , blogDescription])
    return blogdb.submitSingleBlog(blog)

@app.route('/preview', methods=['POST'])
def preview():
    blogTitle = request.form['blogTitle']
    blogContent = request.form['blogContent']
    blogTypeID = request.form['blogTypeID']
    blogKeyWords = request.form['blogKeyWords']
    blogDescription = request.form['blogDescription']
    blog = Blog([1,blogTypeID,blogTitle , blogContent ,int(time.time()) ,0,0,blogKeyWords , blogDescription])
    return render_template('previewBlog.html',blog=blog)

@app.route('/sample/<sampleURL>', methods=['GET'])
def showSample(sampleURL):
    previewUrl = 'sample/'+sampleURL+'.html'
    return render_template(previewUrl)


@app.route('/toModifyBlog/<blogID>', methods=['GET'])
def toModifyBlog(blogID):
    blogDB = BlogDB()
    blogDic = blogDB.getSingleBlog(blogID)
    return render_template('submitBlog.html',blog=blogDic , operationType="MOD")




@app.template_filter('dateToString')
def dateToString(t):
    localDate = date.fromtimestamp(float(t))
    return localDate.isoformat()

@app.template_filter('blogTypeFormat')
def blogTypeFormat(t):
    t = int(t)
    blogTypeDB = BlogTypeDB()
    blogTypes = blogTypeDB.getAllBlogTypes('template')
    blogTypeTitle = ''
    for blogType in blogTypes :
        if blogType['blogTypeID'] == t :
             blogTypeTitle = blogType['blogTypeTitle']
    return blogTypeTitle


if __name__ == '__main__':
    app.debug = True
    app.run()
