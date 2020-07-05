from __future__ import division
from urllib2 import urlopen

html = urlopen("http://www.google.com/")
print html.read()


def check_exception():
    try:
        print('check_exception')
    except Exception, e:
        print e


def check_dict():
    a = {'foo': 'bar'}
    for i in a.items():
        print i

    a.has_key('foo')


def check_xrange():
    for i in xrange(20):
        print i


def check_unicode():
    a = unicode('aaa')
    print a


some_input = raw_input()
