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

def command_injection_in_body(queries):
    payload=random.choice(list(open('payloads/commandinjection.txt'))).rstrip('\n')

    (key,val)=queries[0].split('=')
    val=payload     #"\""+str(val)+"; ifconfig"+"\""
    st=key+'='+val
    
    for q in xrange(1,len(queries)):
        (key,val)=queries[q].split('=')
        val=payload     #"\""+str(val)+"; ifconfig"+"\""
        st+='&'+key+'='+val
    return st

def fuzz_for_command_injection_in_body(req_body):
    queries=[]
    if(req_body):
        queries=map(str,req_body.split('&'))
    if(len(queries)):
        st=command_injection_in_body(queries)
        if(len(st)!=0):
            req_body=st
            print with_color(31, "==== REQUEST BODY ====\n%s\n" % req_body)
    return req_body

def verify_command_injection_in_body(res_body):
    if(res_body.find("127.0.0.1")!=-1): #if(res_body.find("Congratulations")!=-1):
        print with_color(31, "==== RESPONSE BODY ====\n%s\n" % res_body)
        os.kill(os.getpid(), 9)
