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
from gibberbotproperties import GibberbotProperties
from adiumproperties import AdiumProperties

# TODO convert protocol names to a standard format, i.e. prpl-jabber vs. libpurple-Jabber
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
        ispidgin = True
elif os.path.exists(os.path.join(appdir, 'otr.key')) \
    and os.path.exists(os.path.join(appdir, 'otr.fp')):
    islibotr = True
    isirssi = True

if isadium:
    print 'Reading Adium files: '
    keys = AdiumProperties.parse(appdir)
elif isirssi:
    print 'Reading irssi files: '
    keys = OtrPrivateKeys.parse(os.path.join(appdir, 'otr.key'))
    keys += OtrFingerprints.parse(os.path.join(appdir, 'otr.fp'))
elif islibotr:
    print 'Reading libotr files: '
    keys = OtrPrivateKeys.parse(os.path.join(appdir, 'otr.private_key'))
    keys += OtrFingerprints.parse(os.path.join(appdir, 'otr.fingerprints'))
elif isotr4j:
    print 'Reading otr4j format'

if keys:
    pprint.pprint(keys)
    GibberbotProperties.write(keys, 'output')
    OtrFingerprints.write(keys, os.path.join('output', 'otr.fingerprints'))
    OtrPrivateKeys.write(keys, os.path.join('output', 'otr.private_keys'))
