#!/usr/bin/python

'''
   3.14 找出当月的日期范围
   解决：计算范围开始和结束，迭代是利用datetime.timedelta对象 来递增日期。
   calendar 为日历模块  eg. calendar.weekday(year, month, day) 返回日期的日期码 0（星期一）到6（星期日）
'''
from datetime import datetime,date,timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day = 1)
        _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
        end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)

a_day = timedelta(days = 1)
first_day, last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    first_day += a_day

'''
    3.15 将字符串转换为日期

'''
