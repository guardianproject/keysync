#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
from pyparsing import *
from base64 import b64decode
#import pprint

from otr_private_key import OTRPrivateKeys

# TODO get Adium account IDs from ~/Library/Application\ Support/Adium\ 2.0/Users/Default/Accounts.plist
# TODO use python-potr's convertkey.py to convert old libotr files

print OTRPrivateKeys.parse(sys.argv[1])
