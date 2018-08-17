#!/usr/bin/python
#coding=utf8

import os
targetpath = "f:\\"
children = []
show_file = True
try:
    targetpath = targetpath
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
        print {"name": "too many dir", "dirnums": len(pathdir)}
except Exception, e:
    print e
print children