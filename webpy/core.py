import web
from base import *
from system_utils import *

urls = (
    '/', 'index',
    '/info', 'info',
    '/login', 'login',
    '/logout', 'logout',
    '/default', 'default',
    '/settime', 'settime',
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
        return render.info()

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
        
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app.debug = True
    app.run()