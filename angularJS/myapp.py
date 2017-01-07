#-*- coding:utf-8 -*-
__author__ = 'teng.gao'

from flask import Flask, request, render_template
import MySQLdb
from datetime import date

import time
from jinja2 import Environment, FileSystemLoader
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
env = Environment(loader=FileSystemLoader('/templates'))


app = Flask(__name__)

@app.route('/index', methods=['GET', 'POST'])
def home():
    return render_template('first.html')
    

@app.route('/contacts', methods=['GET', 'POST'])
def Page_1():
    return render_template('contacts.html')

@app.route('/contacts/list', methods=['GET', 'POST'])
def Page_2():
    return render_template('contacts.list.html')

@app.route('/contacts/detail', methods=['GET', 'POST'])
def Page_3():
    return render_template('contacts.detail.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run()
