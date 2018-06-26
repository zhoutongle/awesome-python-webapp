#!/usr/bin/env python
#-*- coding: utf-8 -*-
from base import _
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def notify_translation(msg_dict):
    message_info = msg_dict['message']
    if msg_dict['serial'] == "1001":
        message_info = message_info.replace('Cpu usage is too hight, cpu usage reached', _('Cpu usage is too hight, cpu usage reached').decode('utf-8'))
        
    if msg_dict['serial'] == "1002":
        message_info = message_info.replace('Memory usage is too hight, memory usage reached', _('Memory usage is too hight, memory usage reached').decode('utf-8'))
        
    msg_dict['message'] = message_info
