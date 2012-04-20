#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
import os
import struct
import base64
import string
import pprint
from pyparsing import *

import otrapps.util
from otrapps.otr_private_key import OtrPrivateKeys
from otrapps.otr_fingerprints import OtrFingerprints
from otrapps.gibberbotproperties import GibberbotProperties
from otrapps.adiumproperties import AdiumProperties

# TODO merge duplicates in the final keys
# TODO convert protocol names to a standard format, i.e. prpl-jabber vs. libpurple-Jabber
# TODO use python-potr's convertkey.py to convert old libotr files

islibotr = False
isotr4j = False

isjitsi = False
isgibberbot = False
isirssi = False
isadium = False
ispidgin = False

if len(sys.argv) == 0:
    print 'you need to specify file(s) to convert'
    sys.exit()

keys = dict()
for file in sys.argv[1:]:
    appdir = os.path.dirname(file)
    print 'Checking ' + appdir + ':'

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
            ispidgin = True
    elif os.path.exists(os.path.join(appdir, 'otr.key')) \
        and os.path.exists(os.path.join(appdir, 'otr.fp')):
        islibotr = True
        isirssi = True

    if isadium:
        print 'Reading Adium files: '
        tmp = AdiumProperties.parse(appdir)
    elif isirssi:
        print 'Reading irssi files: '
        tmp = OtrPrivateKeys.parse(os.path.join(appdir, 'otr.key'))
        keys += OtrFingerprints.parse(os.path.join(appdir, 'otr.fp'))
    elif islibotr:
        print 'Reading libotr files: '
        tmp = OtrPrivateKeys.parse(os.path.join(appdir, 'otr.private_key'))
        tmp += OtrFingerprints.parse(os.path.join(appdir, 'otr.fingerprints'))
    elif isgibberbot:
        print 'Reading Gibberbot otr4j format'
        tmp = GibberbotProperties.parse(os.path.join(appdir, 'otr_keystore'))
        pprint.pprint(tmp)
    elif isjitsi:
        print 'Reading Jitsi otr4j format'
    keys = tmp
        #for k,v in tmp.items():
        #keys[k] = v

if keys:
    #pprint.pprint(keys)
    GibberbotProperties.write(keys, 'output')
    OtrFingerprints.write(keys, os.path.join('output', 'otr.fingerprints'))
    OtrPrivateKeys.write(keys, os.path.join('output', 'otr.private_keys'))
