#!/usr/bin/python


import os, sys
import json
import urllib2
import urlparse
from shutil import copyfile
from optparse import OptionParser
from contextlib import contextmanager, closing
from pprint import PrettyPrinter
pprint = PrettyPrinter(indent=2).pprint
SCHEMES = { }

"""
contextlib is cool

class Context(object);
    def __init__(self):
        print '__init__'
    def __enter__(self):
        print self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print '__exit__'

with Context() as c:
    print "Test Context"

"""

class Config(object):
    
    def __init__(self):
        self.defaultparamfile = None
        self.parser = OptionParser(usage='%prog [options]...')
        self.parser.add_option('-p', '--paramfile', 
                                dest='paramfile',
                                default=self.defaultparamfile,
                                help='parameter file have all cluster information')
        self.parser.add_option('-v', '--verbose', dest='verbose',
                                action='store_true', help='be verbose')
        self.parser.add_option('-q', '--quiet', dest='quiet',
                                action='store_true', help='be quiet')

    def parseargs(self, args=None):
        self.params = {}
        opts, args = self.parser.parse_args(args)
        self.paramfile = opts.paramfile
        def extractparams(args):
            params = {}
            rem = []
            for arg in args:
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    params[k] = v
                else:
                    rem.append(arg)
            return params, rem
        cliparams, args = extractparams(args)
        if self.paramfile:
            def openurl(url):
                def openfile():
                    if not os.path.exists(url):
                        raise Exception('cannot find file at "%s"' %url)
                    return open(url)
                scheme = urlparse.urlparse(url).scheme
                if not scheme:
                    return openfile()
                openit = SCHEMES.get(scheme, partial(urllib2.urlopen, timeout=60))
                try:
                    f = openit(url)
                    f.__enter__ = lambda: f
                    f.__exit__ = lambda etype, e, tb: e is None
                    return f
                except urllib2.URLError:
                    return openfile()
            def readparams(paramfile):
                try:
                    with closing(openurl(paramfile)) as i:
                        params = self.readparamstring(i.read())
                        params['paramfile'] = paramfile
                        return params
                except urllib2.URLError:
                    raise Exception
            self.params = readparams(self.paramfile)
        return self.params

    def readparamstring(self, s):
        params = {}
        def setparam(k, v):
            try:
                #print 'key: %s, value: %s' %(params[k], json.loads(v))
                params[k] = json.loads(v)
            except ValueError:
                params[k] = v
        l, k, v = None, None, None
        for l in str(s).splitlines():
            if not l or l[0] == '#':
                continue
            if l[0] not in ('\t', ' ', ']', '}'):
                if k:
                    setparam(k, v)
                k, v = l.split('=', 1)
            else:
                v += l
        if l:
            setparam(k, v)
        return params

if __name__ == '__main__':
    inst = Config()
    out = inst.parseargs()
    pprint(out)

