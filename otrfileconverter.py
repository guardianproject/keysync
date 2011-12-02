#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
import os
import struct
import base64
import string
import pprint
from pyparsing import *

import util

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

# TODO get Adium account IDs from ~/Library/Application\ Support/Adium\ 2.0/Users/Default/Accounts.plist
# TODO use python-potr's convertkey.py to convert old libotr files

islibotr = False
isotr4j = False

isjitsi = False
isgibberbot = False
isirssi = False
isadium = False
ispidgin = False

appdir = os.path.dirname(sys.argv[1])

if os.path.exists(os.path.join(appdir, 'otr_keystore')):
    isotr4j = True
    isgibberbot = True
elif os.path.exists(os.path.join(appdir, 'sip-communicator.properties')) \
    and os.path.exists(os.path.join(appdir, 'contactlist.xml')):
    isotr4j = True
    isjitsi = True
elif os.path.exists(os.path.join(appdir, 'otr.private_key')) \
    and os.path.exists(os.path.join(appdir, 'otr.fingerprints')):
    islibotr = True
    if os.path.exists(os.path.join(appdir, 'Accounts.plist')):
        isadium = True
    elif os.path.exists(os.path.join(appdir, 'accounts.xml')):
        isadium = True
elif os.path.exists(os.path.join(appdir, 'otr.key')) \
    and os.path.exists(os.path.join(appdir, 'otr.fp')):
    islibotr = True
    isirssi = True

if islibotr:
    print 'Reading libotr format'
    keys = OtrPrivateKeys.parse(os.path.join(appdir, 'otr.private_key'))
    pprint.pprint(keys)
    for key in keys:
        print '========================================================================'
        print "-------------------- fingerprint --------------------"
        print key['fingerprint']
        print "-------------------- DSA x509 --------------------"
        print util.ExportDsaX509(key)
        print "-------------------- DSA PKCS#8 --------------------"
        print util.ExportDsaPkcs8(key)
    print '========================================================================'
    fingerprints = OtrFingerprints.parse(os.path.join(appdir, 'otr.fingerprints'))
    pprint.pprint(fingerprints)
    for fp in fingerprints:
        print "-------------------- fingerprint --------------------"
        print fp['name'],
        print ': ',
        print fp['fingerprint']

if isotr4j:
    print 'Reading otr4j format'

if isjitsi:
    print 'Reading Jitsi files: '
elif isgibberbot:
    print 'Reading a Gibberbot file: '
elif isirssi:
    print 'Reading irssi files: '
elif isadium:
    print 'Reading Adium files: '
elif ispidgin:
    print 'Reading Pidgin files: '
