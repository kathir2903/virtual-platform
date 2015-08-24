#!/usr/bin/python


import json, sys, os, re
import urlparse
from psphere import client
from psphere import managedobjects
from psphere import errors
from getconfig import Config

class pspherewrapper(object):

    def __init__(self, cfg):
        self.handle = None
        self.server = None
        self.timeout = None

    def connect(self, server, timeout=300):
        assert self.server is not None
        assert self.timeout is not None

def init(cfg, args):
    print cfg
    print "*************"
    print args
    x = pspherewrapper(cfg)
    print dir(x)
    
def get_credentials(vibaseurl):
    #res = urlparse.urlsplit(vibaseurl)
    #hostname = '%s:%d' % (res.hostname, res.port)
    print vibaseurl
get_credentials("http://test")

