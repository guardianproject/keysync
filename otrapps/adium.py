#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import platform
import plistlib
import sys

if __name__ == '__main__':
    sys.path.insert(0, "../") # so the main() test suite can find otrapps module
import otrapps.util
from otrapps.otr_private_key import OtrPrivateKeys
from otrapps.otr_fingerprints import OtrFingerprints

class AdiumProperties():

    path = os.path.expanduser('~/Library/Application Support/Adium 2.0/Users/Default')
    accountsfile = 'Accounts.plist'
    keyfile = 'otr.private_key'
    fingerprintfile = 'otr.fingerprints'
    files = (accountsfile, keyfile, fingerprintfile)

    @staticmethod
    def _get_accounts_from_plist(settingsdir):
        '''get dict of accounts from Accounts.plist'''
        # convert index numbers used for the name into the actual account name
        accountsfile = os.path.join(settingsdir, 'Accounts.plist')
        print('accountsfile: ', end=' ')
        print(accountsfile)
        if not os.path.exists(accountsfile):
            oldaccountsfile = accountsfile
            accountsfile = os.path.join(AdiumProperties.path, AdiumProperties.accountsfile)
            if platform.system() == 'Darwin' and os.path.exists(accountsfile):
                print('Adium WARNING: "' + oldaccountsfile + '" does not exist! Using:')
                print('\t"' + accountsfile + '"')
            else:
                print('Adium ERROR: No usable Accounts.plist file found, cannot create Adium files!')
                return []
        # make sure the plist is in XML format, not binary,
        # this should be converted to use python-biplist.
        if platform.system() == 'Darwin':
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
        for adiumIndex, key in keydict.items():
            for account in accounts:
                if account['ObjectID'] == key['name']:
                    name = account['UID']
                    key['name'] = name
                    newkeydict[name] = key
        keydict = newkeydict

        fpf = os.path.join(settingsdir, AdiumProperties.fingerprintfile)
        if os.path.exists(fpf):
            otrapps.util.merge_keydicts(keydict, OtrFingerprints.parse(fpf))

        return keydict

    @staticmethod
    def write(keydict, savedir='./'):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')

        # need when converting account names back to Adium's account index number
        accountsplist = AdiumProperties._get_accounts_from_plist(savedir)

        kf = os.path.join(savedir, AdiumProperties.keyfile)
        adiumkeydict = dict()
        for name, key in keydict.items():
            name = key['name']
            for account in accountsplist:
                if account['UID'] == name:
                    key['name'] = account['ObjectID']
                    adiumkeydict[name] = key
        OtrPrivateKeys.write(keydict, kf)

        accounts = []
        for account in accountsplist:
            accounts.append(account['ObjectID'])
        fpf = os.path.join(savedir, AdiumProperties.fingerprintfile)
        OtrFingerprints.write(keydict, fpf, accounts)


if __name__ == '__main__':

    import pprint

    print('Adium stores its files in ' + AdiumProperties.path)

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/adium'
    keydict = AdiumProperties.parse(settingsdir)
    pprint.pprint(keydict)

    AdiumProperties.write(keydict, '/tmp')
