#/usr/python

import re
import date

# text_1 = '我昨日早上8点来的' 
# print(date.time_extract(text_1))
# exit()

location_str = ["【起点】塘厦"]
import addressparser
df = addressparser.transform(location_str)
print(df)
exit(0)

import pymysql


str_address ='''【类型】车找人 
【时间】4月24号早上
【起点】塘厦
【终点】上高
【座位】4位子
【电话】13927447458'''
strs = str_address.splitlines(True)
# print(strs)
arr = {}
for x in strs:
	if '车找人' in x:
		arr['type'] = '车找人'
		pass
	if '人找车' in x:
		arr['type'] ='人找车'
		pass
	if '时间' in x:
		d = date.time_extract(x)
		arr['start_time'] = d[0]
		pass
	if '起点' in x:
		df = addressparser.transform([x])
		s = df['省'][0]
		si = df['市'][0]
		area = df['区'][0]
		if len(area)>0:
			arr['start'] = area
		else:
			arr['start'] = si
		pass
	if '终点' in x:
		df1 = addressparser.transform([x])
		s1 = df1['省'][0]
		si1 = df1['市'][0]
		area1 = df1['区'][0]
		if len(area1)>0:
			arr['end'] = area1
		else:
			arr['end'] = si1
		pass
	if '座位' in x:
		m = re.findall("\d+", x)
		if len(m)>0:
			arr['people'] = m[0]
		else:
			arr['people'] = 1
	if '人数' in x:
		m = re.findall("\d+", x)
		if len(m)>0:
			arr['people'] = m[0]
		else:
			arr['people'] = 1
		# print("人数："+ m[0])
		
		pass
	if '电话' in x:
		m = re.findall("\d+", x)
		arr['phone'] = m[0]
		pass
	if '手机' in x:
		m = re.findall("\d+", x)
		arr['phone'] = m[0]
		pass
	pass

print(arr)
arr['name'] = 'bingo'

cols = ", ".join('`{}`'.format(k) for k in arr.keys())
print(cols)  # '`name`, `age`'

val_cols = ', '.join('%({})s'.format(k) for k in arr.keys())
print(val_cols)  # '%(name)s, %(age)s'

sql = "insert into py(%s) values(%s)"
res_sql = sql % (cols, val_cols)
print(res_sql)
# exit(1)

db = pymysql.connect()
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询 
# ctime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
cursor.execute('set profiling = 1')
try:
    cursor.execute(res_sql, arr)
except Exception:
    cursor.execute('show profiles')
    for row in cursor:
        print(row)        
cursor.execute('set profiling = 0')
db.commit()
