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

MONITOR_PATH = currpath + "\\utils\\monitor_reporter.py"
CPU_MEM_PATH = currpath + "\\data\\cpu_mem.txt"
WARN_INFO_PATH = currpath + "\\data\\warn_info.txt"

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
    '/playmusic', 'playmusic',
    '/readbook', 'readbook',
    '/getmovie', 'getmovie'
)

app = web.application(urls, globals())
render=web.template.render('templates')

#i18n
alltranslations = web.storage()
localedir = os.path.join(currpath,'i18n')

def get_translations(lang='zh_CN'):
    if lang in alltranslations:
        translation = alltranslations[lang]
    elif lang is None:
        translation = gettext.NullTranslations()
    else:
        try:
            translation = gettext.translation('messages',localedir,languages=[lang])
        except Exception as e:
            translation = gettext.NullTranslations()
    return translation
    
def load_translations(lang):
    lang = str(lang)
    translation = alltranslations.get(lang)
    if translation is None:
        translation = get_translations(lang)
        alltranslations[lang] = translation

        for lk in alltranslations.keys():
            if lk != lang:
                del alltranslations[lk]
    return translation
    
def custom_gettext(string):
    lang = 'zh_CN'
    if 'session' in globals() and 'user' in globals()['session'] and 'lang' in globals()['session'].user:
        lang = session.user.get('lang')
    translation = load_translations(lang)
    if translation is None:
        return unicode(string)
    return translation.ugettext(string)


#config template
web.template.Template.globals['ELT'] = '$'
web.template.Template.globals['_'] = custom_gettext
_ = custom_gettext

web.config.debug = False
session = web.session.Session(app, web.session.DiskStore('session'))

class index:
    def GET(self):
        content = {"q":"1", "w":"2"}
        return render.index()

class info:
    def GET(self):
        content = get_system_info()
        print(content)
        return render.info(content)

class login:
    def GET(self):
        return render.login()
    def POST(self):
        params = web.input()
        print(params)
        username = params['username']
        password = params['password']
        if username == "Admin" and password == "123456":
            raise web.seeother('/')
        else:
            raise web.seeother('/login')

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
        #content = get_cpu_mem_info()
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
        content = []
        with open(WARN_INFO_PATH, "r") as f:
            content = f.read()
            if content:
                content = eval(content)
            for sub in content:
               notify_translation(sub)
        return render.log(content)

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
        
if __name__ == "__main__":

    subprocess.Popen('python %s >> /dev/null 2>&1' % MONITOR_PATH)
    web.internalerror = web.debugerror
    app.debug = True
    app.run()
    