# -*- coding: utf-8 -*-
import MySQLdb
import json
import time

class DbConnection(object):


	"""本类用于管理数据库连接"""
	def __init__(self, arg):
		self.arg = arg


	@classmethod
	def get_connection_55(self,db_name = 'PS_iQuality' ):
	    _t = dict(host = '10.0.3.55',user = 'iQuser',passwd = 'IQ$User55%', db=db_name)
	    return MySQLdb.connect(host = _t["host"], user = _t["user"], passwd = _t["passwd"], db=_t["db"], connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')


	@classmethod
	def get_connection_175(self,db_name = 'irelease' ):
	    _t = dict(host = '10.0.0.175',user = 'iadmin',passwd = 'itask#ADMIN89', db=db_name)
	    return MySQLdb.connect(host = _t["host"], user = _t["user"], passwd = _t["passwd"], db=_t["db"], connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')


	@classmethod
	def get_connection_local( self ,db_name = 'test' ):
		_t = dict(host = '10.1.151.23',user = 'root',passwd = 'root', db=db_name)
		return MySQLdb.connect(host = _t["host"], user = _t["user"], passwd = _t["passwd"], db=_t["db"], connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')


	@classmethod
	def get_connection_175_imanage(self,db_name = 'imanage' ):
	    _t = dict(host = '10.0.0.175',user = 'iadmin',passwd = 'itask#ADMIN89', db=db_name)
	    return MySQLdb.connect(host = _t["host"], user = _t["user"], passwd = _t["passwd"], db=_t["db"], connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')


	@classmethod
	def get_connection_175_db_conn(self,db_name = 'ilog' ):
	    _t = dict(host = '10.0.0.175',user = 'ilogadmin',passwd = 'SPD@ilogservice99', db=db_name)
	    return MySQLdb.connect(host = _t["host"], user = _t["user"], passwd = _t["passwd"], db=_t["db"], connect_timeout=10,charset='utf8', init_command='SET NAMES UTF8')








