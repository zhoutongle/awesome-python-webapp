#-*-coding: utf-8-*-

import urllib
import urllib2
import re
import sys
import codecs
import json
import os

default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class MOVIE:
    def __init__(self):
        self.index = 0
        self.url = 'https://movie.douban.com/top250?start=%s&filter=' % self.index

    def getPage(self):
        try:
            request = urllib2.Request(self.url)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "连接豆瓣电影失败，错误原因", e.reason
                return None

    def getPageItems(self):
        movie_list = []
        while self.index < 250:
            self.url = self.url.split("?")[0] + "?start=%s&filter=" % self.index
            pageCode = self.getPage()
            pattern = re.compile('<em class="">(.*?)</em>.*?<span class="title">(.*?)</span>.*?<p class="">(.*?)</p>.*?average">(.*?)</span>.*?<span>(.*?)</span>.*?<span class="inq">(.*?)</span>', re.S)
            items = re.findall(pattern, pageCode)
            for item in items:
                temp = {}
                #info = "序号：%s\n电影名称：%s\n其他：%s\n评分：%s\n评价数：%s\n描述：%s\n"% (item[0].strip(), item[1].strip(), item[2].strip().replace("&nbsp;", "").replace("<br>", ""), item[3].strip(), item[4].strip(), item[5].strip())
                #with open("../models/movie1.txt", "a+") as f:
                #    f.write("%s\n" % info)
                temp['index']      = item[0].strip()
                temp['movie_name'] = item[1].strip().encode("utf-8")
                temp['other']      = item[2].strip().replace("&nbsp;", "").replace("<br>", "").encode("utf-8")
                temp['grade']      = item[3].strip().encode("utf-8")
                temp['number']     = item[4].strip().encode("utf-8")
                temp['describe']   = item[5].strip().encode("utf-8")
                movie_list.append(temp)
            self.index += 25
        #电影写到文件里
        #os.getcwd()
        #os.chdir(r'd:\EasyUI\models')
        #with open("movie.txt", "w") as f:
        #    f.write(json.dumps(movie_list, ensure_ascii=False))
        return json.dumps(movie_list, ensure_ascii=False)
if __name__ == "__main__":
    movie = MOVIE()
    movie.getPageItems()
    #with open("../models/movie.txt", "r") as f:
    #    data = eval(f.read())
    #print data[0]['movie_name']