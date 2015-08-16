#!/usr/bin/python


import json, sys, os, re
import urlparse
from psphere import client
from psphere import managedobjects
from psphere import errors
from getconfig import Config

#class pspherewrapper(object):
def init(cfg, args):
    print cfg
    print "*************"
    print args
def get_credentials(vibaseurl):
    #res = urlparse.urlsplit(vibaseurl)
    #hostname = '%s:%d' % (res.hostname, res.port)
    print vibaseurl
get_credentials("http://test")

