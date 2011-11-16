#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
from pyparsing import *
from base64 import b64decode
#import pprint

from otr_private_keys import OTRPrivateKeys

# TODO get Adium account IDs from ~/Library/Application\ Support/Adium\ 2.0/Users/Default/Accounts.plist

print OTRPrivateKeys.parse(sys.argv[1])
