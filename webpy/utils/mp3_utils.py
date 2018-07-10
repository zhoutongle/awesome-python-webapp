#!/usr/bin/python
#coding=utf8
import mp3play
import pygame
import time

music = None

class Music():
    def __init__(self, filename):
        self.filename = filename
        self.main = mp3play.load(self.filename)
    def play(self):
        self.main.play()
    def stop(self):
        self.main.stop()
    def isplaying(self):
        return self.main.isplaying()
    def ispaused(self):
        return self.main.ispaused()
    def pause(self):
        self.main.pause()
    def unpause(self):
        self.main.unpause()
    def music_tims(flag=True):
        if flag:
            return self.main.seconds()
        else:
            return self.main.milliseconds()
            
def play_music(flag):
    try:
        print flag
        global music
        if music == None:
            filename = u"C:\\Users\\Administrator\\Music\\123.mp3"
            music = mp3play.load(filename)
        else:
            print music.isplaying()
        if flag == "play":
            print music, music.isplaying()
            music.play()
            print music, music.isplaying()
        elif flag == "stop":
            #music.play()
            print music
            music.stop()
            #music = ""
            print music, music.isplaying()
        elif flag == "pause":
            music.pause()
        elif flag == "unpause":
            music.unpause()
    except Exception, e:
        print e

def play_music(flag):
    filename = u"C:\\Users\\Administrator\\Music\\123.mp3"
    if flag == "play":
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    elif flag == "stop":
        if pygame.mixer.music.get_busy() == 1:
            pygame.mixer.music.stop()
    elif flag == "pause":
        if pygame.mixer.music.get_busy() == 1:
            pygame.mixer.music.pause()
    elif flag == "unpause":
        pygame.mixer.music.unpause()