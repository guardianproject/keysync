#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import plistlib
import sys

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

class AdiumProperties():

    path = os.path.expanduser('~/Library/Application Support/Adium 2.0/Users/Default')

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = AdiumProperties.path
        keys = OtrPrivateKeys.parse(os.path.join(settingsdir, 'otr.private_key'))
        keys += OtrFingerprints.parse(os.path.join(settingsdir, 'otr.fingerprints'))
        accountsfile = os.path.join(settingsdir, 'Accounts.plist')
        # make sure the plist is in XML format, not binary
        os.system("plutil -convert xml1 '" + accountsfile + "'")
        accounts = plistlib.readPlist(accountsfile)['Accounts']
        for key in keys:
            for account in accounts:
                if account['ObjectID'] == key['name']:
                    key['name'] = account['UID']
        return keys

    @staticmethod
    def write():
        print 'AdiumProperties.write() is not implemented'


if __name__ == '__main__':

    import pprint

    print 'Adium stores its files in ' + AdiumProperties.path

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = 'tests/adium'
    l = AdiumProperties.parse(settingsdir)
    pprint.pprint(l)
