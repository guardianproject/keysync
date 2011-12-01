#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
import os
import struct
import base64
import string
from pyparsing import *

import util

from otr_private_key import OTRPrivateKeys

# TODO get Adium account IDs from ~/Library/Application\ Support/Adium\ 2.0/Users/Default/Accounts.plist
# TODO use python-potr's convertkey.py to convert old libotr files

otrfile = sys.argv[1]
filename = os.path.basename(otrfile)

f = open(otrfile, 'r')
otrdata = ""
for line in f.readlines():
    otrdata += line

if filename == 'otr_keystore':
    print 'Reading a Gibberbot file: '
elif filename == 'sip-communicator.properties':
    print 'Reading a Jitsi file: '
elif filename == 'otr.private_key':
    keys = OTRPrivateKeys.parse(otrdata)
    for key in keys:
        print "\n\n-------------------- fingerprint --------------------"
        print key['fingerprint']
        print "-------------------- DSA x509 --------------------"
        print util.ExportDsaX509(key)
        print "-------------------- DSA PKCS#8 --------------------"
        print util.ExportDsaPkcs8(key)
