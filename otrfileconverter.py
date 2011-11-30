#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
import os
import struct
import base64
import string
from pyparsing import *
from Crypto.PublicKey import DSA

import util

from otr_private_key import OTRPrivateKeys

# TODO get Adium account IDs from ~/Library/Application\ Support/Adium\ 2.0/Users/Default/Accounts.plist
# TODO use python-potr's convertkey.py to convert old libotr files

otrfile = sys.argv[1]
filename = os.path.basename(otrfile)

if filename == 'otr_keystore':
    print 'Reading a Gibberbot file: '
elif filename == 'sip-communicator.properties':
    print 'Reading a Jitsi file: '
elif filename == 'otr.private_key':
    keys = OTRPrivateKeys.parse(otrfile)

    for key in keys:
        if key[0] == "account":
            print '-------------------'
            for element in key:
                #print element
                if element[0] == "name":
                    print "Name: ",
                    print element[1]
                elif element[0] == "protocol":
                    print "Protocol: ",
                    print element[1]
                elif element[0] == "private-key":
                    if element[1][0] == 'dsa':
                        keydict = {}
                        print "Key: "
                        for num in element[1][1:6]:
                            keydict[num[0]] = num[1]
                            if num[0] == 'y':
                                y = num[1]
                            elif num[0] == 'g':
                                g = num[1]
                            elif num[0] == 'p':
                                p = num[1]
                            elif num[0] == 'q':
                                q = num[1]
                            elif num[0] == 'x':
                                x = num[1]
                            print '\t' + num[0],
                            print num[1]
                        #dsa = DSA.construct((y, g, p, q, x))
                        #print dsa.publickey()
                        print "-------------------- DSA x509 --------------------"
                        print util.ExportDsaX509(keydict)
                        print "-------------------- DSA PKCS#8 --------------------"
                        print util.ExportDsaPkcs8(keydict)
