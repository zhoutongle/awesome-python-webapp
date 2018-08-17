import web
import os
from base import *
import simplejson
import datetime
import subprocess
from time import sleep
import random
import xlwt
import json

currpath = os.path.join(os.getcwd(), os.path.dirname(__file__))
if not currpath in sys.path:
    sys.path.append(currpath)
    
utilspath = os.path.join(currpath, 'utils')
if not utilspath in sys.path:
    sys.path.append(utilspath)

from system_utils import *
from cpu_utils import *
from notify_utils import *
from mp3_utils import *
from read_utils import *
from get_models import *
from find_utils import *
from base import _, session

MONITOR_PATH = currpath + "\\utils\\monitor_reporter.py"
CPU_MEM_PATH = currpath + "\\data\\cpu_mem.txt"
WARN_INFO_PATH = currpath + "\\data\\warn_info.txt"
USER_PASSWD_PATH = currpath + "\\data\\user_passwd.txt"

urls = (
    '/', 'index',
    '/info', 'info',
    '/login', 'login',
    '/logout', 'logout',
    '/settime', 'settime',
    '/getdisk', 'getdisk',
    '/getdiskinfoa', 'getdiskinfoa',
    '/geticoninfo', 'geticoninfo',
    '/getcpuinfo', 'getcpuinfo',
    '/getcpuinfoa', 'getcpuinfoa',
    '/getlog', 'getlog',
    '/deletelog', 'deletelog',
    '/getmusic', 'getmusic',
    '/playmusic', 'playmusic',
    '/readbook', 'readbook',
    '/getmovie', 'getmovie',
    '/getuser', 'getuser',
    '/adduser', 'adduser',
    '/deleteuser', 'deleteuser',
    '/getgeo', 'getgeo',
    '/modifypassword', 'modifypassword',
    '/moviedownload', 'moviedownload',
    '/getdirectory', 'getdirectory'
)

app = web.application(urls, globals())
render=web.template.render('templates')
session = web.session.Session(app, web.session.DiskStore('session'))
#config debug
web.config.debug = False

class index:
    def GET(self):
        num = 0
        content = []
        with open(WARN_INFO_PATH, "r") as f:
            content = f.read()
            if content:
                content = eval(content)
        num = len(content)
        return render.index(num)

class info:
    def GET(self):
        content = get_system_info()
        print content
        return render.info(content)

class login:
    def GET(self):
        return render.login([])
    def POST(self):
        try:
            params = web.input()
            content = []
            with open(USER_PASSWD_PATH, "r") as f:
                file_content = f.read()
                if file_content:
                    content = eval(file_content)
            username = params['username']
            password = params['password']
            for user in content:
                if username == user['username']:
                    if password == user["password"]:
                        # print session.keys(), session.values()
                        # session.user = {}
                        # session.user.id = 1
                        # session.user.name = username
                        # session.user.passwd = password
                        # print session.keys(), session.values()
                        return 0
                    else:
                        return _("password is error")
            return _("user does not exist")
        except Exception as e:
            print traceback.format_exc()

class logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/login')

class settime:
    def GET(self):
        return render.settime()
        
class modifypassword:
    def GET(self):
        params = web.input()
        content = {}
        content['currentuser'] = params['currentuser']
        return render.modifypassword(content)
    def POST(self):
        params = web.input()
        username = params['username']
        password0 = params['password0']
        password1 = params['password1']
        content = []
        with open(USER_PASSWD_PATH, "r") as f:
            file_content = f.read()
            if file_content:
                content = eval(file_content)
        for user in content:
            if username == user['username']:
                if password0 == user["password"]:
                    user["password"] = password1
                    with open(USER_PASSWD_PATH, "w") as f:
                        f.write("%s" % content)
                    return 0
                else:
                    return _("password is error")
        return _("user does not exist")
        
class getdisk:
    def GET(self):
        content = get_system_info()
        return render.getdisk(content)

class getdiskinfoa:
    def GET(self):
        content = get_disk_info()
        return simplejson.dumps(content)

class geticoninfo:
    def GET(self):
        return render.geticoninfo()

class getcpuinfo:
    def GET(self):
        return render.getcpuinfo()
        
class getcpuinfoa:
    def GET(self):
        content = []
        with open(CPU_MEM_PATH, "r") as  f:
            file_content = f.read()
        if file_content:
            content = eval(file_content)
        if len(content) > 30:
            content = content[len(content)-30:]
        return simplejson.dumps(content)

class getlog:
    def GET(self):
        data = {}
        content = []
        with open(WARN_INFO_PATH, "r") as f:
            content = f.read()
            if content:
                content = eval(content)
            for sub in content:
               notify_translation(sub)
        data['loglist'] = content
        data['num'] = len(content)
        return render.log(data)
        
class deletelog:
    def POST(self):
        params = web.input(loglist=[])
        content = []
        loglist = params['loglist']
        with open(WARN_INFO_PATH, "r") as f:
            file_content = f.read()
            if file_content:
                content = eval(file_content)
                for sub in content[::]:
                    if sub['time'] in loglist:
                        content.remove(sub)
                with open(WARN_INFO_PATH, "w") as f:
                    f.write("%s" % content)
            else:
                return _("log")
        return 0
        
class getmusic:
    def GET(self):
        content = []
        music = []
        music = find_file(".mp3", "f:\\")
        music1 = find_file(".mp3", "e:\\")
        music2 = find_file(".mp3", "d:\\")
        music3 = find_file(".mp3", "c:\\")
        music.extend(music1)
        music.extend(music2)
        music.extend(music3)
        return render.getmusic(music)

class playmusic:
    def POST(self):
        params = web.input()
        flag = params['flag']
        musicname = params['musicname']
        musicname = musicname.replace("/", "\\\\")
        play_music(flag, musicname)
        return 0
        
class readbook:
    def GET(self):
        content = []
        return render.readbook(content)
    def POST(self):
        file_content = ""
        params = web.input()
        file_content = params['info']
        filepath = params['filepath']
        if filepath:
            with open(filepath, 'r') as f:
                file_content = f.read()
        print file_content
        say_word(file_content)
        return 0
        
class getmovie:
    def GET(self):
        movie = MOVIE()
        content = movie.getPageItems()
        content = eval(content)
        return render.getmovie(content)

class getuser:
    def GET(self):
        content = []
        with open(USER_PASSWD_PATH, "r") as f:
            file_content = f.read()
        if file_content:
            content = eval(file_content)
        return render.getuser(content)
        
class adduser:
    def GET(self):
        return render.adduser()
    def POST(self):
        params = web.input()
        content = []
        user = {}
        with open(USER_PASSWD_PATH, "r") as f:
            file_content = f.read()
        if file_content:
            content = eval(file_content)
        for sub in content:
            if sub['username'] == params['username']:
                return _('this user is exist')
        user['username'] = params['username']
        user['password'] = params['password']
        user['mail'] = params['mail']
        content.append(user)
        with open(USER_PASSWD_PATH, "w") as f:
            f.write("%s" % content)
        return 0

class deleteuser:
    def POST(self):
        params = web.input(userlist=[])
        content = []
        userlist = params['userlist']
        with open(USER_PASSWD_PATH, "r") as f:
            file_content = f.read()
            if file_content:
                content = eval(file_content)
                for sub in content[::]:
                    if sub['username'] in userlist:
                        content.remove(sub)
                with open(USER_PASSWD_PATH, "w") as f:
                    f.write("%s" % content)
            else:
                return _("user")
        return 0
       
class getgeo:
    def GET(self):
        return render.getgeo()
        
class moviedownload:
    def POST(self):
        filename = currpath + "movie_info_" + datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S_%f") + ".xls"           
        return 0
        
class getdirectory:
    def GET(self):
        content = []
        return render.getdirectory(content)
    def POST(self):
        params = web.input()
        targetpath = params['path']
        children = []
        show_file = True
        try:
            pathlist = os.listdir(targetpath)
            pathdir = []
            for i in range(len(pathlist)):
                pathlist[i] = pathlist[i]
            pathlist.sort()
            for path in pathlist:
                if path.find('.') == 0:
                    continue
                if not show_file:
                    subpath = os.path.join(targetpath, path)
                    if os.path.isdir(subpath):
                        pathdir.append(subpath)
                        children.append({"name": path, "path": subpath, "isParent":"true"})
                else:
                    subpath = os.path.join(targetpath, path)
                    pathdir.append(subpath)
                    if os.path.isdir(subpath):
                        if subpath.find("internal_op") < 0:
                            children.append({"name": path, "path": subpath, "isParent":"true"})
                    else:
                        children.append({"name": path, "path": subpath, "isParent":"false"})
            if len(pathdir) > 20000:
                return {"name": "too many dir", "dirnums": len(pathdir)}
        except Exception, e:
            print e
        return simplejson.dumps(children)
        
if __name__ == "__main__":
    try:
        ret = subprocess.Popen('python %s >> /dev/null 2>&1' % MONITOR_PATH)
        web.internalerror = web.debugerror
        app.debug = True
        app.run()
    except Exception, e:
        console.log("----------- %s" % traceback.format_exc())
    