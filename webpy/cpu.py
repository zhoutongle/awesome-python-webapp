#coding=utf8  
import psutil  
cpu = {'user' : 0, 'system' : 0, 'idle' : 0, 'percent' : 0}  
mem = {'total' : 0, 'avaiable' : 0, 'percent' : 0, 'used' : 0, 'free' : 0}  
  
#磁盘名称  
disk_id = []  
#将每个磁盘的total used free percent 分别存入到相应的list  
disk_total = []  
disk_used = []  
disk_free = []  
disk_percent = []
disk = []
unit_list = ['B', 'KB', "MB", "GB", "PB"]
  
#获取CPU信息  
def get_cpu_info():  
    cpu_times = psutil.cpu_times()  
    cpu['user'] = cpu_times.user  
    cpu['system'] = cpu_times.system  
    cpu['idle'] = cpu_times.idle  
    cpu['percent'] = psutil.cpu_percent(interval=2)
    
#获取内存信息  
def get_mem_info():
    mem_info = psutil.virtual_memory()  
    mem['total'] = mem_info.total  
    mem['available'] = mem_info.available  
    mem['percent'] = mem_info.percent  
    mem['used'] = mem_info.used  
    mem['free'] = mem_info.free  
#获取磁盘  
def get_disk_info():
    for id in psutil.disk_partitions():
        temp = {}
        if 'cdrom' in id.opts or id.fstype == '':  
            continue  
        disk_name = id.device.split(':')  
        s = disk_name[0]  
        #disk_id.append(s)
        disk_info = psutil.disk_usage(id.device)  
        #disk_total.append(disk_info.total)  
        #isk_used.append(disk_info.used)  
        #disk_free.append(disk_info.free)  
        #disk_percent.append(disk_info.percent)
        temp['id']    = s
        temp['info']  = psutil.disk_usage(id.device)
        if disk_info.used > disk_info.free:
            temp0 = disk_info.free
            temp1 = disk_info.used
            temp2 = disk_info.total
            unit_num = 0
            while temp0 > 1024:
                temp0 = temp0/1024
                unit_num += 1
                print unit_num
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
            tepm2 = disk_info.total
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