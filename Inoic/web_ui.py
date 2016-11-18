#-*- coding:utf-8 -*-
import json
import time
import sys
import os
import urllib
from flask import Flask, render_template, request, send_from_directory,redirect,url_for ,  make_response
from datetime import date, datetime 
import ast
import json
import math
import xlwt
import xlrd
import StringIO

app = Flask(__name__)


@app.route('/index', methods=['GET'])
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0',port=6060)

