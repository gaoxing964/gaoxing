#-*- coding:utf-8 -*-
import time
from dao import ErrorMessageManager , LoginMessageManager
import json
import sys
import os
from flask import Flask, flash, redirect, render_template,  request, url_for



app = Flask(__name__)
app.debug = True

@app.route('/login_log')
def login_log():
	'''记录登录请求'''
	result = dict(status=200, data="", message="")
	project_id = request.args.get('project_id','')
	logging_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
	username = request.args.get('username','')
	data = {
	    'project_id' : project_id ,
	    'logging_time' : logging_time ,
	    'username' : username
	}
	LoginMessageManager.insertLoginMessage(data)
	return json.dumps(result)

def GetNowTime():
    datetime = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    return datetime
	
	
@app.route('/report/visitorSummary', methods=['GET'])
def visitor_summary():
    '''更改指定项目Owner'''
    result = dict(status=200, data="", message="")
    search_data = {
            "visitor":request.args.get('visitor', ''),
            "project_id":request.args.get('project_id', ''),
            "startDate":request.args.get('start_date', '2016-10-01'),
            "endDate":request.args.get('end_date', ''),
            "summaryType":request.args.get('summaryType', 'day')
            }
    if not search_data['endDate']:
        datetime = GetNowTime()
        search_data['endDate'] = datetime
    result_data, result_username_num, total_visitor = VisitorSum.determine_type(search_data)
    result['data'] = result_data
    result['user_count'] = result_username_num
    result['total_visitor'] = total_visitor
    return json.dumps(result)



if __name__ == "__main__":
	try:
	    pid = os.fork()
	    if pid > 0:
	        sys.exit(0)
	except OSError:
	    report( "unable to fork: %s" % sys.exc_info()[1])
	    raise
	
	from werkzeug.contrib.fixers import ProxyFix
	from flup.server.fcgi import WSGIServer
	app.wsgi_app = ProxyFix(app.wsgi_app)
	WSGIServer(app, bindAddress=('0.0.0.0', 5080)).run()