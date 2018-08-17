#!/usr/bin/python
#coding=utf8

import sys
import pyttsx

reload(sys)
sys.setdefaultencoding('utf-8')

def say_word(content):
    engine = pyttsx.init()
    engine.say(content)
    engine.runAndWait()

