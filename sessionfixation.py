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
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from cStringIO import StringIO
from subprocess import Popen, PIPE
from HTMLParser import HTMLParser
from random import randint

overflowstrings = ["A" * 8192]

def with_color(c, s):
    return "\x1b[%dm%s\x1b[0m" % (c, s)

def sessionfixation_in_header(req):
    cookie = req.headers.get('Cookie', '')
    if(len(cookie)):
        (cookie_key,cookie_val)=cookie.split('=')
        cookielength=len(cookie_val)
        cookie_val='A'*cookielength
    else:
        cookie_key="JSESSIONID"
        cookie_val='A'*32
    req.headers['Cookie']=str(cookie_key)+"="+str(cookie_val)

def sessionfixation_in_url(queries):
    (key,val)=queries[0].split('=')
    if("ID" in key or "id" in key):
        val='A'*32
    st=key+'='+val

    for q in xrange(1,len(queries)):
        (key,val)=queries[q].split('=')
        if("ID" in key or "id" in key):
            val='A'*32
        st+='&'+key+'='+val
    return st

def fuzz_for_sessionfixation_in_url(req):
    u = urlparse.urlsplit(req.path)
    queries=[]
    if(u.query):
        queries=map(str,u.query.split('&'))
        if(len(queries)):
            st=sessionfixation_in_url(queries)
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
            st=sessionfixation_in_url(queries)
            if(len(st)!=0):
                s,t=req.path.split(';')
                if(len(t)!=0):
                    req.path=s+';'+st
                else:
                    req.path=s+st

    return req.path

def verify_sessionfixation(res, res_body):
    cookie = res.headers.get('Set-Cookie', '')
    (cookie_key,cookie_val)=cookie.split('=')
    cookielength=len(cookie_val)
    sentcookie="AAAAAAAAAA" #'A'*cookielength
    if(sentcookie in cookie_val):
        print with_color(31, "==== SessionFixation in Header ====\n%s\n" % res.headers)
    elif(sentcookie in res_body):
        print with_color(31, "==== SessionFixation in Body ====\n%s\n" % res_body)
