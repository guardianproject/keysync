#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import plistlib
import sys
import util

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

class AdiumProperties():

    path = os.path.expanduser('~/Library/Application Support/Adium 2.0/Users/Default')
    keyfile = 'otr.private_key'
    fingerprintfile = 'otr.fingerprints'

    @staticmethod
    def _get_accounts_from_plist(settingsdir):
        '''get dict of accounts from Accounts.plist'''
        # convert index numbers used for the name into the actual account name
        accountsfile = os.path.join(settingsdir, 'Accounts.plist')
        # make sure the plist is in XML format, not binary
        os.system("plutil -convert xml1 '" + accountsfile + "'")
        return plistlib.readPlist(accountsfile)['Accounts']

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = AdiumProperties.path

        kf = os.path.join(settingsdir, AdiumProperties.keyfile)
        if os.path.exists(kf):
            keydict = OtrPrivateKeys.parse(kf)
        else:
            keydict = dict()

        accounts = AdiumProperties._get_accounts_from_plist(settingsdir)
        newkeydict = dict()
        for adiumIndex, key in keydict.iteritems():
            for account in accounts:
                if account['ObjectID'] == key['name']:
                    name = account['UID']
                    key['name'] = name
                    newkeydict[name] = key
        keydict = newkeydict

        fpf = os.path.join(settingsdir, AdiumProperties.fingerprintfile)
        if os.path.exists(fpf):
            util.merge_keydicts(keydict, OtrFingerprints.parse(fpf))

        return keydict

    @staticmethod
    def write(keydict, savedir='./'):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')

        kf = os.path.join(savedir, AdiumProperties.keyfile)
        OtrPrivateKeys.write(keydict, kf)

        accounts = []
        accountsplist = AdiumProperties._get_accounts_from_plist(settingsdir)
        for account in accountsplist:
            accounts.append(account['ObjectID'])
        fpf = os.path.join(savedir, AdiumProperties.fingerprintfile)
        OtrFingerprints.write(keydict, fpf, accounts)


if __name__ == '__main__':

    import pprint

    print 'Adium stores its files in ' + AdiumProperties.path

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/adium'
    keydict = AdiumProperties.parse(settingsdir)
    pprint.pprint(keydict)

    AdiumProperties.write(keydict, '/tmp')
