import web
from base import *
from system_utils import *
from cpu import *
urls = (
    '/', 'index',
    '/info', 'info',
    '/login', 'login',
    '/logout', 'logout',
    '/settime', 'settime',
    '/getdisk', 'getdisk',
    '/getdiskinfoa', 'getdiskinfoa',
)

app = web.application(urls, globals())
render=web.template.render('templates')

allowed = (
    ('Admin', '123456'),
)
web.config.debug = False
session = web.session.Session(app, web.session.DiskStore('session'))

class index:
    def GET(self):
        content = {"q":"1", "w":"2"}
        return render.index()

class info:
    def GET(self):
        content = get_system_info()
        return render.info(content)

class login:
    def GET(self):
        return render.login()
    def POST(self):
        params = web.input()
        print params
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
        print(content)
        return content
        
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app.debug = True
    app.run()