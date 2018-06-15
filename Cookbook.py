#!/usr/bin/python
# coding: utf-8

'''
   3.14 找出当月的日期范围
   解决：计算范围开始和结束，迭代是利用datetime.timedelta对象 来递增日期。
   calendar 为日历模块  eg. calendar.weekday(year, month, day) 返回日期的日期码 0（星期一）到6（星期日）
'''
print("=====================  3.14  ===========================")
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

def date_range(start, end, step):
    while start < end:
        yield start
        start += step

for d in date_range(datetime(2018, 9, 1), datetime(2018, 9, 4), timedelta(hours=6)):
    print(d)

'''
    3.15 将字符串转换为日期
    解决： 使用python中的标准模块datetime
    >>> from datetime import datetime
    >>> text = '2018-06-07'
    >>> y = datetime.strptime(text, '%Y-%m-%d')
    >>> z = datetime.now()
    >>> diff = z - y
    >>> diff
    datetime.timedelta(0, 36511, 991444)
    strptime()性能比较差,如果知道时间的格式，下面的函数比datetime.strptime()快了7倍多
'''
from datetime import datetime
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))

'''代码中使用获得2018-6-7 10:26:00格式的时间'''
import time
timer = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
print(timer)

'''
    3.16 处理涉及到时区的日期问题
    解决：都使用pytz模块，提供了奥尔森时区数据库
    转换为UTC时间
'''
from datetime import datetime
from pytz import timezone
import pytz

d = datetime(2018, 6, 7, 16, 9, 0)
print(d)

#Localize the date for Chicago 芝加哥
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)

#Convert to Bangalore time 同一时间班加罗尔时间
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print(bang_d)

utc_d = loc_d.astimezone(pytz.utc)
print(utc_d)

later_utc = utc_d + timedelta(minutes=30)
print(later_utc.astimezone(central))

print(pytz.country_timezones['IN'])

'''
    4.1 手动访问迭代器中的元素
    解决：手动访问，可以使用next（）函数

'''
print("=====================  4.1  ===========================")
#with open('D:\\test\\awesome-python-webapp\\readme.txt') as f:
with open('readme.txt') as f:
    try:
        while True:
            line = next(f)
            print(line)
    except StopIteration:
        pass

#with open('D:\\test\\awesome-python-webapp\\readme.txt') as f:
with open('readme.txt') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line)

'''
    4.2 委托迭代
    解决： 定义一个__iter__()方法，将迭代请求委托到对象内部持有的容器上
'''
print("=====================  4.2  ===========================")
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    #def depth_first(self):
    #    yield self
    #    for c in self:
    #        yield from c.depth_first()

#Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)
        #Outputs Node(1), Node(2)

'''
   4.3 用生成器创建新的迭代模式

'''
print("=====================  4.3  ===========================")
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

print(list(frange(0, 1, 0.125)))
for n in frange(0, 4, 0.5):
    print(n)

def countdown(n):
    print('Starting to count from', n)
    while n > 0:
        yield n
        n -= 1
    print('Done!')

# Create the generator, notice no output appears
c = countdown(3)
print(c)

# Run to first yield and emit a value
next(c)

# Run to the next yield
next(c)

# Run to next yield
next(c)

# Run to next yield (iteration stops)
#next(c)

'''
    4.4 实现迭代协议
'''
print("=====================  4.4  ===========================")
# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    #for ch in root.depth_first():
    #    print(ch)
        # Output Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)

class Node1:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, other_node):
        self._children.append(other_node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        return DepthFirstIterator(self)

class DepthFirstIterator(object):
    '''
        Depth-first traversal
    '''
    def __init__(self, start_node):
        self._node = start_node
        self.children_iter = Node
        self._hild_iter = Node

    def __iter__(self):
        return self

    def __next__(self):
        # Return myself if just started; creaetean iterator for children
        if self.children_iter is None:
            self._children_iter = iter(self._node)
            return self._node
        
        # If processing a child, return its next item
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)

        # Advance to the next child and start its iteration
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)

"""
    4.5 反向迭代
    解决：可以使用内建的reversed()函数实现反向迭代。
"""
print("=====================  4.5  ===========================")
a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)

#反向打印文件里的内容,将可迭代对象转成列表可能会消耗大量内存。
f = open('readme.txt')
for line in reversed(list(f)):
    print(line)

#实现__reversed__()方法，可以用于自定义的类上面。
class Countdown:
    def __init__(self, start):
        self.start = start

    #Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    #Reverse iterator
    def __reversed__():
        n = 1
        while n <= self.start:
            yield n
            n += 1

"""
    4.6 定义带有额外状态的生成器
    解决：把生成器函数代码放到__iter__()方法中。
"""
print("=====================  4.6  ===========================")
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

with open('Cookbook.py') as f:
    lines = linehistory(f)
    for line in lines:
        if "python" in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline))

"""
    4.7 对迭代器做切片操作
    解决：对迭代器和生成器做切片操作，itertools.iislice()函数是完美的选择。
"""
print("=====================  4.7  ===========================")
def count(n):
    while n < 100:
        yield n
        n += 1
c = count(0)
#print(c[10:20])

import itertools
for x in itertools.islice(c, 10, 20):
    print(x)

"""
    4.8 跳过可迭代对象中的前一部分元素
    解决：使用itertools模块中的itertools.dropwhile()函数。
"""
print("=====================  4.8  ===========================")
from itertools import dropwhile
with open("readme.txt") as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line)

from itertools import islice
items = ['a', 'b', 'c', 'd', '1', '4', '10']
for x in islice(items, 3, None):
    print(x)

with open("readme.txt") as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line)

"""
    4.9 迭代所有可能的组合或排列
    解决：itertools模块提供了3各函数，
    第一个是itertools.permutations(), 6种 {1,2,3},{1,3,2},{2,1,3},{2,3,1},{3,2,1},{3,1,2}
    第二个是itertools.combinations(), 1种 {1,2,3}
    第三个是itertools.combinations_with_replacement(), 10种{1,1,1},{1,1,2},{1,1,3},{2,2,2},{2,2,1},{2,2,3},{3,3,3},{3,3,1},{3,3,2},{1,2,3}

"""
print("=====================  4.9  ===========================")
items = ['a', 'b', 'c']
from itertools import permutations
for p in permutations(items):
    print(p)

for p in permutations(items, 2):
    print(p)

from itertools import combinations
for c in combinations(items, 3):
    print(c)

for c in combinations(items, 2):
    print(c)

from itertools import combinations_with_replacement
for c in combinations_with_replacement(items, 3):
    print(c)

"""
    4.10 以索引-值对的的形式迭代序列
    解决：使用内建的enumerate()函数
"""
print("=====================  4.10  ===========================")
my_list = ["a", "b", "c"]
for idx, val in enumerate(my_list, 1):
    print(idx, val)

