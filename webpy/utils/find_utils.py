# coding=utf-8
import os
import sys  
 
 
def print_dirName(content, spath, mp3_list):
    for schild in os.listdir(spath):  
        schildpath = spath+'/'+schild  
        if os.path.isdir(schildpath):  
            print_dirName(content, schildpath, mp3_list)  
        else:  
            if content in schildpath:
                mp3_list.append(schildpath.decode('gbk'))

def find_file(content, spath):
    try:
        mp3_list = []
        print_dirName(content, spath, mp3_list)
    except Exception, e:
        pass
    return mp3_list