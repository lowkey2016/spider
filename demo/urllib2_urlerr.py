#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
 
# URL Error
# requset = urllib2.Request('http://www.xxxxx.com')
# try:
#     urllib2.urlopen(requset, timeout = 10)
# except urllib2.URLError, e:
#     print e.reason


# HTTP Error
# req = urllib2.Request('http://blog.csdn.net/cqcre')
# try:
#     urllib2.urlopen(req)
# except urllib2.HTTPError, e:
#     print e.code
#     print e.reason

 
req = urllib2.Request('http://blog.csdn.net/cqcre')
try:
    urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.code
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
else:
    print "OK"
