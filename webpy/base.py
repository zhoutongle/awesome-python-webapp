#*- coding: utf-8 -*-
#base.py

import os
import sys
import time
import gettext
import traceback
import simplejson
import re
import json
import subprocess
import web
from urls import urls

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
SESSION_PATH = currpath + "\\session"
TEMPLATEDIR = os.path.join(currpath,'template')
JSTEMPLATEDIR = os.path.join(currpath,'js')
stow = web.storage
render = web.template.render(TEMPLATEDIR,cache=False)
jsrender = web.template.render(JSTEMPLATEDIR,cache=False)
debug=True
layout='default'

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

#config session
web.config.session_parameters['cookie_name'] = "ztl"
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 1800 #30 * 60, 30minutes
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['ignore_change_ip'] = False
web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
web.config.session_parameters['expired_message'] = 'Session expired'

app_info = {
    'mapping':urls,
    'fvars':globals(),
}
app = web.application(**app_info)
session_info = {
    'app':app,
    'store':web.session.DiskStore(SESSION_PATH),
    'initializer':{
        'user':stow({
            'id':None,
            'name':None,
            'skin':'redmond',
            'lang':'zh_CN'
        }),
        'runtime':stow({
            'node':'',
            'unit':'',
            'service':'',
            'managercheck':False
        }),
        'global_v':stow({
            'rlist':list(),
            'new_msg_num':0
        })
    }}

def _init_session():
    if web.config.get('_session') is None:
        session = web.session.Session(**session_info)
        web.config._session = session
    else:
        session = web.config._session
    return session
session = _init_session()

#config debug
web.config.debug = False

class Page:
    def __init__(self):
        self.request_method = web.ctx.env.get('REQUEST_METHOD')
        self.path = web.ctx.env.get('PATH_INFO')
        self.setup = stow({})
        self.content = stow({})
        #self.skin = session.user.skin
        self.params = web.input(file=[])


    #def _valid(self):
    #    if not session.user.id:
    #        if self.path and self.path not in ['/login']:
    #            pass
    #        raise web.seeother('/login?redirect_url=%s' % self.path)

    def _render(self,ajax=False,layout='default'):
        #self.content.skin = self.skin
        #self.content.session = session
        self.page_content = render.__getattr__(self.setup['template'])(self.content)
        #self._jsrender()
        if ajax:
            return self.page_content
        page_setup = {
            #'title':settings.procname,
            #'footer':settings.footer,
            'breadcrumbs':[],
            'menu_title':'',
            'menus':[],
            'currmenu':'',
            'javascript':[],
            'jstemplate':[],
            'css':[],
            'skin':self.skin
        }
        for key,value in page_setup.iteritems():
            self.setup[key] = key in self.setup and self.setup[key] or value
        self.shortcuts = fun_gen_shotcuts(self.setup['breadcrumbs'])
        self.menu_items = func_gen_menu(self.setup['menus'])
        setup_oem()
        #if session.user.name == 'admin':
        #    self.navigators = admin_menue
        #elif session.user.name != 'anonymous':
        #    self.navigators = admin_menue
        #else:
        #    self.navigators = anonymous_menue
        content = stow({
            'page_setup':self.setup,
            'menu_items':self.menu_items,
            'shortcuts':self.shortcuts,
            'navigators':self.navigators,
            'page_content':self.page_content,
            'oem_params': oem_params,
            #'session':session,
        })
        return render.__getattr__(layout)(content)

    def _jsrender(self):
        self.setup['javascript_files'] = []
        if not 'jstemplate' in self.setup:
            self.setup['jstemplate']= []
            self.setup['jstemplate'].append('utils.js')
            self.setup['jstemplate'].append('datatable_ZH.js')
            self.setup['jstemplate'].append('pythonsysinfo.js')
        else:
            self.setup['jstemplate'].append('utils.js')
            self.setup['jstemplate'].append('datatable_ZH.js')
            self.setup['jstemplate'].append('pythonsysinfo.js')
        if 'jstemplate' in self.setup:
            import os
            for file in self.setup['jstemplate']:
                jsfile = ''
                jsfilename = ''
                if os.path.splitext(file)[1] == '.js':
                    if os.path.splitext(file)[0] != 'datatable_ZH':
                        jsfile = file
                    else:
                        jsfile = os.path.splitext(file)[0]
                    jsfilename = os.path.splitext(file)[0]
                else:
                    jsfile = file + '.js'
                    jsfilename = file
                try:
                    js_content = jsrender.__getattr__(jsfilename)(self.content)
                    jsfilepath = os.path.join(settings.JSTEMPPATH,jsfile)
                    #utils.upload_file(settings.JSTEMPPATH,jsfilepath,js_content)
                    f = open(os.path.join(settings.JSTEMPPATH,jsfilepath),'w')
                    f.write(str(js_content))
                    f.close()
                    self.setup['javascript_files'].append(jsfile)
                except Exception,e:
                    self.setup['javascript_files'].append(jsfile)

    def render(self,ajax=False,debug=debug,layout=layout,notemplate=False,valid=True):
        if debug:
            if valid:
                self._valid()
            if notemplate:
                return self._logic()
            self._logic()
            return self._render(ajax,layout)
        else:
            try:
                if valid:
                    self._valid()
                if notemplate:
                    return self._logic()
                self._logic()
                return self._render(ajax,layout)
            except Exception,e:
                pass
    def _logic(self):
        self.content = stow({})
        self.setup = stow({

        })

    def _action(self):
        self.redirect_url = '/'
        raise web.seeother(self.redirect_url)

    def action(self,ajax=False,debug=debug):
        if debug:
            if ajax:
                return self._action()
            self._action()
        else:
            try:
                if ajax:
                    return self._action()
                self._action()
            except Exception,e:
                pass
