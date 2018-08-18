#!/usr/bin/python
# -*- coding: utf-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  # 设置默认编码格式为'utf-8'


import re
import requests
from bs4 import BeautifulSoup

def test(qq):
    return unicode(qq, "utf-8").encode('gbk')
kv = {'user-agent': 'Mozilla/5.0'}

def find_train(train_data, from_station, to_station):
    train_info = []
    url1 = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9006'
    response1 = requests.get(url1, headers=kv)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response1.text)
    sta_cod = dict(stations)                        # 车站名称对应的代码
    cod_sta = {v : k for k, v in sta_cod.items()}    # 代码对应的车站名称
    
    while 1:    # 多次查询
        k = [0, 0, 0]
        while sum(k) != 3:
            #train_data = raw_input(test("请输入出发时间(格式:20180131):"))
            #from_station = raw_input(test("请输入出发站:"))
            #to_station = raw_input(test("请输入到达站:"))
            train_data = '20180819'
            from_station = '北京'
            to_station = '郑州'
            if len(train_data) == 8:
                tra_dat = train_data[0:4] + '-' + train_data[4:6] + '-' + train_data[6:8]
                year = eval(train_data[0:4])
                if eval(train_data[4]) != 0:
                    month = eval(train_data[4:6])
                else:
                    month = eval(train_data[5])
                if eval(train_data[6]) != 0:
                    day = eval(train_data[6:8])
                else:
                    day = eval(train_data[7])
                if month < 1 or month > 12 or day < 0 or day > 31:
                    print('出发日期输入错误！')
                elif month in [1, 3, 5, 7, 8, 10, 12]:
                    k[0] = 1
                elif month in [4, 6, 9, 11]:
                    if day < 31:
                        k[0] = 1
                    else:
                        print('出发日期输入错误！')
                else:
                    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                        if day < 30:
                            k[0] = 1
                        else:
                            print('出发日期输入错误！')
                    else:
                        if day < 29:
                            k[0] = 1
                        else:
                            print('出发日期输入错误！')
            else:
                print('出发日期输入错误！')
     
            if from_station.find('站') == -1:
                k[1] = 1
                from_station = sta_cod[from_station.decode('utf-8')]
            elif from_station.find('站') != -1:
                k[1] = 1
                from_station = sta_cod[from_station[0:(len(from_station) - 1)]]
            else:
                print(test('出发站输入错误！'))
     
            if to_station.find('站') == -1:
                k[2] = 1
                to_station = sta_cod[to_station.decode('utf-8')]
            elif to_station.find('站') != -1:
                k[2] = 1
                to_station = sta_cod[to_station[0:(len(to_station) - 1)]]
            else:
                print(test('到达站输入错误！'))
        # 火车票信息查询接口
        url2 = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' + tra_dat + '&leftTicketDTO.from_station=' + from_station + '&leftTicketDTO.to_station=' + to_station + '&purpose_codes=ADULT'
        response2 = requests.get(url2, headers=kv)
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        Str_tmp = str(soup2)    # 将获得的网页源码转换成字符串
        
        Str = Str_tmp.replace("true", "'true'")
        k = []
        k_tmp = -1
        Mes = eval(Str)         # 字符串转换成字典
        if Mes['messages']:
            print(test('选择的查询日期不在预售日期范围内！\n'))
        elif Mes['data']['result'] == [] and Mes['messages'] ==[]:
            print('很抱歉，按您的查询条件，当前未找到从 {:} 到 {:} 的列车！\n'.format(cod_sta[from_station], cod_sta[to_station]))
        else:
            mes = Mes['data']['result']
            tra_cod = []  # 车次
            sta_beg = []  # 始发站
            sta_end = []  # 终到站
            sta_lea = []  # 起始站
            sta_arr = []  # 终点站
            t_lea = []    # 出发时间
            t_arr = []    # 到达时间
            t_dur = []    # 历时
            t_dat = []    # 出发日期
            tic = []      # 是否有票
            gr = []       # 高级软卧
            rw = []       # 软卧
            rz = []       # 软座
            wz = []       # 无座
            yw = []       # 硬卧
            yz = []       # 硬座
            edz = []      # 二等座
            ydz = []      # 一等座
            swz = []      # 商务座
            dw = []       # 动卧
     
            for i in range(0, len(mes)):    # 根据字符串特征提取相关信息
                for j in range(0, len(mes[i])):
                    k_tmp = mes[i].find('|', k_tmp + 1)
                    if k_tmp == -1:
                        break
                    k.append(k_tmp)
                tra_cod.append(mes[i][(k[2] + 1):k[3]])
                sta_beg.append(cod_sta[mes[i][(k[3] + 1):k[4]]])
                sta_end.append(cod_sta[mes[i][(k[4] + 1):k[5]]])
                sta_lea.append(cod_sta[mes[i][(k[5] + 1):k[6]]])
                sta_arr.append(cod_sta[mes[i][(k[6] + 1):k[7]]])
                t_lea.append(mes[i][(k[7] + 1):k[8]])
                t_arr.append(mes[i][(k[8] + 1):k[9]])
                t_dur.append(mes[i][(k[9] + 1):k[10]])
                tic.append(mes[i][(k[10] + 1):k[11]])
                t_dat.append(mes[i][(k[12] + 1):k[13]])
                gr.append(mes[i][(k[20] + 1):k[21]])
                rw.append(mes[i][(k[22] + 1):k[23]])
                rz.append(mes[i][(k[23] + 1):k[24]])
                wz.append(mes[i][(k[25] + 1):k[26]])
                yw.append(mes[i][(k[27] + 1):k[28]])
                yz.append(mes[i][(k[28] + 1):k[29]])
                edz.append(mes[i][(k[29] + 1):k[30]])
                ydz.append(mes[i][(k[30] + 1):k[31]])
                swz.append(mes[i][(k[31] + 1):k[32]])
                dw.append(mes[i][(k[32] + 1):k[33]])
                for h in range(0, len(gr)):     # 表示列车不存在相关票种
                    if gr[h].strip() == '':
                        gr[h] = '--'
                    if rw[h].strip() == '':
                        rw[h] = '--'
                    if rz[h].strip() == '':
                        rz[h] = '--'
                    if wz[h].strip() == '':
                        wz[h] = '--'
                    if yw[h].strip() == '':
                        yw[h] = '--'
                    if yz[h].strip() == '':
                        yz[h] = '--'
                    if edz[h].strip() == '':
                        edz[h] = '--'
                    if ydz[h].strip() == '':
                        ydz[h] = '--'
                    if swz[h].strip() == '':
                        swz[h] = '--'
                    if dw[h].strip() == '':
                        dw[h] = '--'
                k_tmp = -1
                del k[0:(len(k) + 1)]
            #输出格式统一
            # tplt = "{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}"
            # print(tplt.format(test("车次"), test("车站"), test("时间"), test("历时"), test("商务座"), test("一等座"), test("二等座"), test("高级软卧"), test("软卧"), test("动卧"), test("硬卧"), test("软座"), test("硬座"), test("无座")))
            # for i in range(0, len(mes)):
               # print(tplt.format(tra_cod[i], sta_lea[i], t_lea[i], t_dur[i], swz[i], ydz[i], edz[i], gr[i], rw[i], dw[i],yw[i], rz[i], yz[i], wz[i]))
               # print(tplt.format("", sta_arr[i], t_arr[i], "", "", "", "", "", "", "", "", "", "", ""))
               # print("")
            for i in range(0, len(mes)):
                temp = {}
                temp['tra_cod'] = tra_cod[i]
                temp['sta_lea'] = sta_lea[i]
                temp['t_lea'] = t_lea[i]
                temp['t_dur'] = t_dur[i]
                temp['swz'] = swz[i]
                temp['ydz'] = ydz[i]
                temp['edz'] = edz[i]
                temp['gr'] = gr[i]
                temp['rw'] = rw[i]
                temp['dw'] = dw[i]
                temp['yw'] = yw[i]
                temp['rz'] = rz[i]
                temp['yz'] = yz[i]
                temp['wz'] = wz[i]
                train_info.append(temp)
            return train_info