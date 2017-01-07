#-*- coding:utf-8 -*-
from dbConnection import DbConnection
import time
import pdb
import MySQLdb


class ErrorMessageManager(object):


    @classmethod
    def  insertErrorMessage(self, data):
		conn = DbConnection.get_connection_55()
		cursor = conn.cursor()  
		try:
			sql = ''' insert into project_errors (error_description , project_id , error_time) values ( %s , %s , %s ) '''

			cursor.execute(sql , (data['error_description'] , data['project_id'] , data['error_time'] ))
		except Exception as e:
		    print str(e)
		conn.commit()
		cursor.close()
		conn.close()
		
		
		
class LoginMessageManager(object):
	
	@classmethod
	def insertLoginMessage(self, data):
		conn = DbConnection.get_connection_55()
		cursor = conn.cursor()  
		try:
			sql = ''' insert into project_logging_log (username , project_id , loginTime) values ( %s , %s , %s ) '''

			cursor.execute(sql , (data['username'] , data['project_id'] , data['logging_time'] ))
		except Exception as e:
		    print str(e)
		conn.commit()
		cursor.close()
		conn.close()
		
		
		

class VisitorSum(object):
    """docstring for VisitorSum"""
    def __init__(self, arg):
        super(VisitorSum, self).__init__()
        self.arg = arg
        
    @classmethod
    def determine_type(cls, search_data):
        #根据类型判断是日,周,月
        summaryType = search_data['summaryType']
        if summaryType=='day':
            result_data = VisitorSum.visitorSumbyday(search_data)
            result_username_num = VisitorSum.get_username_num_visitory_Sum_by_day(search_data)
        elif summaryType=='week':
            result_data = VisitorSum.visitorSumbyWeek(search_data)
            result_username_num = VisitorSum.get_username_num_visitory_Sum_by_week(search_data)
        else:
            result_data = VisitorSum.visitorSumbyMonth(search_data)
            result_username_num = VisitorSum.get_username_num_visitory_Sum_by_month(search_data)

        total_visitor = VisitorSum.query_all_visitory()

        return result_data, result_username_num, total_visitor


    @classmethod
    def get_datetime_between_start_and_end(cls, search_data):
        import datetime
        start = search_data['startDate']
        end = search_data['endDate']
        datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
        dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
        result = []
        while datestart<dateend:
            datestart+=datetime.timedelta(days=1)
            date = datestart.strftime('%Y-%m-%d')
            result.append(date)
        result.append(start)
        
        return result


    @classmethod
    def query_all_visitory(cls):        
        conn = DbConnection.get_connection_55( )
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)        
        sql = "SELECT COUNT(DISTINCT(username)) as count from cmcc_page_access_personnel_records"
        cursor.execute(sql)
        result_data, = cursor.fetchall()        

        return result_data
       

    @classmethod
    def get_username_num_visitory_Sum_by_month(cls, search_data):        
        date_list = VisitorSum.get_datetime_between_start_and_end(search_data)
        months = VisitorSum.deal_Month_data(date_list)                
        conn = DbConnection.get_connection_55( )
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        args = (search_data['startDate'], search_data['endDate'])
        sql = "SELECT COUNT(DISTINCT(username)) as count,month(FROM_UNIXTIME(access_time, '%%Y-%%m-%%d')) AS months \
        FROM cmcc_page_access_personnel_records where FROM_UNIXTIME(access_time, '%%Y-%%m-%%d') BETWEEN %s and %s GROUP BY months"
        cursor.execute(sql, args)
        result_data = cursor.fetchall()
        result_data = list(result_data)
        result = []
        for j in range(0, len(result_data)):
            result.append(result_data[j]['months'])        
        ret = [ i for i in months if i not in result ]
        if ret:
            for r in ret:
                one_record = dict(months=r,
                                  count=0
                                 )
                result_data.append(one_record)

        return result_data

       
    @classmethod
    def get_username_num_visitory_Sum_by_week(cls, search_data):
        date_list = VisitorSum.get_datetime_between_start_and_end(search_data)
        week = VisitorSum.deal_week_data(date_list)
        conn = DbConnection.get_connection_55( )
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        args = (search_data['startDate'], search_data['endDate'])
        sql = "SELECT COUNT(DISTINCT(username)) as count, WEEKOFYEAR(FROM_UNIXTIME(access_time, '%%Y-%%m-%%d')) AS WEEKOFYEAR \
        FROM cmcc_page_access_personnel_records where FROM_UNIXTIME(access_time, '%%Y-%%m-%%d') \
        BETWEEN %s and %s GROUP BY WEEKOFYEAR"
        cursor.execute(sql, args)
        result_data = cursor.fetchall()
        result_data = list(result_data)
        result = []
        for j in range(0, len(result_data)):
            result.append(result_data[j]['WEEKOFYEAR'])        
        ret = [ i for i in week if i not in result ]
        if ret:
            for r in ret:
                one_record = dict(WEEKOFYEAR=r,
                                  count=0
                                 )
                result_data.append(one_record)

        return result_data


    @classmethod
    def get_username_num_visitory_Sum_by_day(cls, search_data):
        date_list = VisitorSum.get_datetime_between_start_and_end(search_data)
        conn = DbConnection.get_connection_55( )
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        args = (search_data['startDate'], search_data['endDate'])
        sql = "SELECT COUNT(DISTINCT(username)) as count, FROM_UNIXTIME(access_time, '%%Y-%%m-%%d') AS access_date \
        FROM cmcc_page_access_personnel_records where FROM_UNIXTIME(access_time, '%%Y-%%m-%%d') BETWEEN %s and %s GROUP BY access_date"
        cursor.execute(sql, args)
        result_data = cursor.fetchall()
        result_data = list(result_data)
        result = []
        for j in range(0, len(result_data)):
            result.append(result_data[j]['access_date'])        
        ret = [ i for i in date_list if i not in result ]
        if ret:
            for r in ret:
                one_record = dict(access_date=r,
                                  count=0
                                 )
                result_data.append(one_record)

        return result_data
       

    @classmethod
    def visitorSumbyday(cls, search_data):
        date_list = VisitorSum.get_datetime_between_start_and_end(search_data)
        conn = DbConnection.get_connection_55( )
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        args = (search_data['startDate'], search_data['endDate'])        
        sql = '''SELECT t.access_date as access_date, t.web_url as web_url, count(id) as num from \
        (SELECT *, FROM_UNIXTIME(access_time, "%%Y-%%m-%%d") AS access_date FROM cmcc_page_access_personnel_records where '''
        if search_data['visitor']:
            sql += ''' username="'''+search_data['visitor']+'''" and '''
        sql += '''FROM_UNIXTIME(access_time, "%%Y-%%m-%%d") BETWEEN %s and %s) t GROUP BY t.access_date, t.web_url'''
        cursor.execute(sql, args)
        result_data = cursor.fetchall()
        result_data = list(result_data)
        result = []
        for j in range(0,len(result_data)):
            result.append(result_data[j]['access_date'])        
        ret = [ i for i in date_list if i not in result ]
        if ret:
            for r in ret:
                one_record = dict(access_date=r,
                                  web_url=0,
                                  num=0
                                 )
                result_data.append(one_record)
        deal_result = []
        for k in range(0,len(result_data)):
            sum_login, sum_home, sum_other,flag = 0, 0, 0, 0
            if deal_result:
                for deal in deal_result:
                    if result_data[k]['access_date'] == deal['access_date']:
                        flag = 1
            if flag == 0:
                for l in range(0,len(result_data)):
                    if result_data[k]['access_date'] == result_data[l]['access_date']:
                        if result_data[l]['web_url'] == 'login.html':
                            num = result_data[l]['num']
                            sum_login += num
                        elif result_data[l]['web_url'] == 'home.html':
                            num = result_data[l]['num']
                            sum_home += num
                        else:
                            num = result_data[l]['num']
                            sum_other += num
                one_record_deal = dict(access_date=result_data[k]['access_date'],
                                       sum_login=sum_login,
                                       sum_home=sum_home,
                                       sum_other=sum_other
                                      )
                deal_result.append(one_record_deal)

        return deal_result


    @classmethod
    def deal_week_data(cls, date_list):
        week = []
        for date in date_list:
            date_time = dt.strptime(date,'%Y-%m-%d')
            date_week =date_time.isocalendar()[1]
            week.append(date_week)
        week = list(set(week))

        return week


    @classmethod
    def visitorSumbyWeek(cls, search_data):
        conn = DbConnection.get_connection_55()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        date_list = VisitorSum.get_datetime_between_start_and_end(search_data)
        week = VisitorSum.deal_week_data(date_list)
        args = (search_data['startDate'], search_data['endDate'])
        sql = '''SELECT t.WEEKOFYEAR as WEEKOFYEAR,t.web_url as web_url, count(id) as num \
        from (SELECT *,WEEKOFYEAR(FROM_UNIXTIME(access_time, "%%Y-%%m-%%d")) AS WEEKOFYEAR \
        FROM cmcc_page_access_personnel_records WHERE '''
        if search_data['visitor']:
            sql += ''' username="'''+search_data['visitor']+'''" and '''
        sql += '''FROM_UNIXTIME(access_time, "%%Y-%%m-%%d") BETWEEN %s and %s)t GROUP BY t.WEEKOFYEAR,t.web_url'''
        cursor.execute(sql, args)
        result_data = cursor.fetchall()
        result_data = list(result_data)
        result = []
        for j in range(0,len(result_data)):
            result.append(result_data[j]['WEEKOFYEAR'])
        ret = [ i for i in week if i not in result ]
        if ret:
            for r in ret:
                one_record = dict(WEEKOFYEAR=r,
                                  web_url=0,
                                  num=0
                                 )
                result_data.append(one_record)
        deal_result = []
        for k in range(0,len(result_data)):
            sum_login, sum_home, sum_other,flag = 0, 0, 0, 0
            if deal_result:
                for deal in deal_result:
                    if result_data[k]['WEEKOFYEAR'] == deal['WEEKOFYEAR']:
                        flag = 1
            if flag == 0:
                for l in range(0,len(result_data)):
                    if result_data[k]['WEEKOFYEAR'] == result_data[l]['WEEKOFYEAR']:
                        if result_data[l]['web_url'] == 'login.html':
                            num = result_data[l]['num']
                            sum_login += num
                        elif result_data[l]['web_url'] == 'home.html':
                            num = result_data[l]['num']
                            sum_home += num
                        else:
                            num = result_data[l]['num']
                            sum_other += num
                one_record_deal = dict(WEEKOFYEAR=result_data[k]['WEEKOFYEAR'],
                                       sum_login=sum_login,
                                       sum_home=sum_home, 
                                       sum_other=sum_other
                                      )
                deal_result.append(one_record_deal) 

        return deal_result


    @classmethod
    def deal_Month_data(cls, date_list):
        import time
        months = []       
        for date in date_list:
            nowDate = time.strptime(date, "%Y-%m-%d")
            month = nowDate.tm_mon
            months.append(month)
       
        months = list(set(months))
        return months


    @classmethod
    def visitorSumbyMonth(cls, search_data):
        conn = DbConnection.get_connection_55()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        date_list = VisitorSum.get_datetime_between_start_and_end(search_data)
        months = VisitorSum.deal_Month_data(date_list)
        args = (search_data['startDate'], search_data['endDate'])
        sql = '''SELECT t.MONTHS AS MONTHS, t.web_url AS web_url, count(id) AS num \
        FROM (SELECT *, MONTH(FROM_UNIXTIME(access_time, "%%Y-%%m-%%d")) AS MONTHS \
        FROM cmcc_page_access_personnel_records WHERE '''
        if search_data['visitor']:
            sql += ''' username="'''+search_data['visitor']+'''" and '''
        sql += '''FROM_UNIXTIME(access_time, "%%Y-%%m-%%d") BETWEEN %s AND %s) t GROUP BY t.MONTHS, t.web_url'''
        cursor.execute(sql, args)
        result_data = cursor.fetchall()
        result_data = list(result_data)
        result = []       
        for j in range(0,len(result_data)):
            result.append(result_data[j]['MONTHS'])

        ret = [ i for i in months if i not in result ]
        if ret:
            for r in ret:
                one_record = dict(MONTHS=r,
                                  web_url=0,
                                  num=0
                                 )
                result_data.append(one_record)
        deal_result = []
        for k in range(0,len(result_data)):
            sum_login, sum_home, sum_other,flag = 0, 0, 0, 0
            if deal_result:
                for deal in deal_result:
                    if result_data[k]['MONTHS'] == deal['MONTHS']:
                        flag = 1
            if flag == 0:
                for l in range(0,len(result_data)):
                    if result_data[k]['MONTHS'] == result_data[l]['MONTHS']:
                        if result_data[l]['web_url'] == 'login.html':
                            num = result_data[l]['num']
                            sum_login += num
                        elif result_data[l]['web_url'] == 'home.html':
                            num = result_data[l]['num']
                            sum_home += num
                        else:
                            num = result_data[l]['num']
                            sum_other += num
                one_record_deal = dict(MONTHS=result_data[k]['MONTHS'],
                                       sum_login=sum_login,
                                       sum_home=sum_home, 
                                       sum_other=sum_other
                                      )
                deal_result.append(one_record_deal) 

        return deal_result
    

    @classmethod
    def get_all_visitor_pm_info(cls, search_data):
        '''获取用户信息'''       
        conn = DbConnection.get_connection_175_imanage()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        pm_list = VisitorSum.get_all_pm_info()
        subName = search_data['q'].strip().replace('.', ' ').lower()
        subName = "%"+subName+"%"
        user  = []
        for p_user in pm_list:
            p_user = "'"+p_user.strip().replace('.', ' ').lower()+"'"
            user.append(p_user)       
        user = ','.join(user)
        args = ()
        sql = "SELECT LOWER(EName) as EName, Name FROM User_List where EName in ("+user+")"
        if search_data['q']:
            sql += " and EName like %s or Name like %s"
            args = (subName, subName)
        cursor.execute(sql, args)
        result_data = cursor.fetchall()       

        cursor.close()
        conn.close()

        return result_data


    @classmethod
    def get_all_pm_info(cls):
        '''获取PM即所有能登录到此系统的人'''
        conn = DbConnection.get_connection_55()
        cursor = conn.cursor()
        result = []
        sql = "SELECT DISTINCT(username) as username from permission"
        cursor.execute(sql)
        for row in cursor.fetchall():
            username, = row
            result.append(username)
        
        return result


