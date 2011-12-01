#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
import os
import struct
import base64
import string
from pyparsing import *

import util

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

# TODO get Adium account IDs from ~/Library/Application\ Support/Adium\ 2.0/Users/Default/Accounts.plist
# TODO use python-potr's convertkey.py to convert old libotr files

otrfile = sys.argv[1]
filename = os.path.basename(otrfile)

if filename == 'otr_keystore':
    print 'Reading a Gibberbot file: '
elif filename == 'sip-communicator.properties':
    print 'Reading a Jitsi file: '
elif filename == 'otr.private_key' or filename == 'otr.key':
    print 'Reading a libotr private key file'
    keys = OtrPrivateKeys.parse(otrfile)
    for key in keys:
        print "-------------------- fingerprint --------------------"
        print key['fingerprint']
        print "-------------------- DSA x509 --------------------"
        print util.ExportDsaX509(key)
        print "-------------------- DSA PKCS#8 --------------------"
        print util.ExportDsaPkcs8(key)
elif filename == 'otr.fingerprints' or filename == 'otr.fp':
    print 'Reading a libotr private key file'
    keys = OtrFingerprints.parse(otrfile)
    for key in keys:
        print "-------------------- fingerprint --------------------"
        print key['name'],
        print ': ',
        print key['fingerprint']

