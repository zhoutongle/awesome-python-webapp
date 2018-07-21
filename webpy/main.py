import web
import os
from base import *
import simplejson
import datetime
import subprocess

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
from base import _

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
    '/playmusic', 'playmusic',
    '/readbook', 'readbook',
    '/getmovie', 'getmovie',
    '/getuser', 'getuser',
    '/adduser', 'adduser'
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
                        return 0
                    else:
                        return _("password is error")
            return _("user does not exist")
        except Exception as e:
            print traceback.format_exc

class logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/login')

class settime:
    def GET(self):
        return render.settime()

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

class playmusic:
    def GET(self):
        content = []
        return render.playmusic(content)
    def POST(self):
        params = web.input()
        flag = params['flag']
        play_music(flag)
        
class readbook:
    def GET(self):
        content = []
        return render.readbook(content)
        
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

if __name__ == "__main__":
    try:
        ret = subprocess.Popen('python %s >> /dev/null 2>&1' % MONITOR_PATH)
        web.internalerror = web.debugerror
        app.debug = True
        app.run()
    except Exception, e:
        console.log("----------- %s" % traceback.format_exc())
    