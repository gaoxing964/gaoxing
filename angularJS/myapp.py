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
    return render_template('create_directive/first.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
