#!/usr/bin/python
#coding=utf8
import psutil
import datetime
import simplejson
#cpu = {'user' : 0, 'system' : 0, 'idle' : 0, 'percent' : 0}  
mem = {'total' : 0, 'avaiable' : 0, 'percent' : 0, 'used' : 0, 'free' : 0}  
  
#磁盘名称  
#disk_id = []  
#将每个磁盘的total used free percent 分别存入到相应的list  
disk_total = []  
disk_used = []  
disk_free = []  
disk_percent = []
#disk = []
unit_list = ['B', 'KB', "MB", "GB", "PB"]
  
#获取CPU信息  
def get_cpu_info():
    cpu = []
    temp = {}
    #cpu_times = psutil.cpu_times()  
    #cpu['user'] = cpu_times.user  
    #cpu['system'] = cpu_times.system  
    #cpu['idle'] = cpu_times.idle  
    temp['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp['percent'] = psutil.cpu_percent(interval=2)
    with open("F:\\awesome-python-webapp\\webpy\\config\\cpu.txt", "r") as  f:
        a = f.read()
    if a:
        cpu = eval(a)
        if len(cpu) > 30:
            cpu = cpu[len(cpu)-30:]
    cpu.append(temp)
    with open("F:\\awesome-python-webapp\\webpy\\config\\cpu.txt", "w") as  f:
        f.write("%s"%cpu)
    return cpu
    
#获取内存信息  
def get_mem_info():
    mem = []
    temp = {}
    mem_info = psutil.virtual_memory()  
    temp['total'] = mem_info.total  
    temp['available'] = mem_info.available  
    temp['percent'] = mem_info.percent  
    temp['used'] = mem_info.used  
    temp['free'] = mem_info.free
    temp['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("F:\\awesome-python-webapp\\webpy\\config\\mem.txt", "r") as  f:
        a = f.read()
    if a:
        mem = eval(a)
        if len(mem) > 30:
            mem = mem[len(mem)-30:]
    mem.append(temp)
    with open("F:\\awesome-python-webapp\\webpy\\config\\mem.txt", "w") as  f:
        f.write("%s"%mem)
    return mem

#合并信息
def get_cpu_mem_info():
    info = []
    temp = {}
    temp['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp['cpu_percent'] = psutil.cpu_percent(interval=2)
    mem_info = psutil.virtual_memory()
    temp['mem_percent'] = mem_info.percent
    with open("F:\\awesome-python-webapp\\webpy\\config\\cpu_mem.txt", "r") as  f:
        a = f.read()
    if a:
        info = eval(a)
        if len(info) > 30:
            info = info[len(info)-30:]
    info.append(temp)
    with open("F:\\awesome-python-webapp\\webpy\\config\\cpu_mem.txt", "w") as  f:
        f.write("%s"%info)
    info.append(temp)
    return info
       
#获取磁盘  
def get_disk_info():
    disk = []
    for id in psutil.disk_partitions():
        temp = {}
        if 'cdrom' in id.opts or id.fstype == '':  
            continue  
        disk_name = id.device.split(':')  
        #s = disk_name[0]  
        #disk_id.append(s)
        disk_info = psutil.disk_usage(id.device)  
        #disk_total.append(disk_info.total)  
        #isk_used.append(disk_info.used)  
        #disk_free.append(disk_info.free)  
        #disk_percent.append(disk_info.percent)
        temp['id']    = disk_name[0]
        temp['info']  = psutil.disk_usage(id.mountpoint)
        if disk_info.used > disk_info.free:
            temp0 = disk_info.free
            temp1 = disk_info.used
            temp2 = disk_info.total
            unit_num = 0
            while temp0 > 1024:
                temp0 = temp0/1024
                unit_num += 1
            temp['free'] = int(str(temp0).split("L")[0])
            temp['unit'] = unit_list[unit_num]
            while unit_num > 0:
                temp1 = temp1/1024
                temp2 = temp2/1024
                unit_num -= 1
            temp['total']  = int(str(temp2).split("L")[0])
            temp['used']  = int(str(temp1).split("L")[0])
        else:
            temp0 = disk_info.used
            temp1 = disk_info.free
            temp2 = disk_info.total
            unit_num = 0
            while temp0 > 1024:
                temp0 = temp0/1024
                unit_num += 1
            temp['used'] = int(str(temp0).split("L")[0])
            temp['unit'] = unit_list[unit_num]
            while unit_num > 0:
                temp1 = temp1/1024
                temp2 = temp2/1024
                unit_num -= 1
            temp['total']  = int(str(temp2).split("L")[0])
            temp['free']  = int(str(temp1).split("L")[0])
        temp['percent'] = disk_info.percent
        disk.append(temp)
    return disk

if __name__ == '__main__':

    #磁盘名称  
    disk_id = []  
    #将每个磁盘的total used free percent 分别存入到相应的list  
    disk_total = []  
    disk_used = []  
    disk_free = []  
    disk_percent = []    

    get_cpu_info()
    cpu_status = cpu['percent']  
    print u"CPU使用率: %s %%" % cpu  
    get_mem_info()  
    mem_status = mem['percent']  
    print u"内存使用率: %s %%" % mem_status      
    get_disk_info()
    for i in range(len(disk_id)):  
        print u'%s盘空闲率: %s %%' % (disk_id[i],100 - disk_percent[i])  
    #raw_input("Enter enter key to exit