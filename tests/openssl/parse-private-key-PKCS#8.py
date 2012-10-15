#!/usr/bin/python

import pyjavaproperties
import imp

errors = imp.load_source('errors', '../../otrapps/errors.py')
util = imp.load_source('util', '../../otrapps/util.py')

filename = 'dsa-key.properties'
p = pyjavaproperties.Properties()
p.load(open(filename))
for item in p.items():
    if item[0] == 'privateKey':
        privdict = util.ParsePkcs8(item[1])
        print 'privdict: ',
        print privdict
    elif item[0] == 'publicKey':
        pubdict = util.ParseX509(item[1])
        print 'pubdict: ',
        print pubdict
