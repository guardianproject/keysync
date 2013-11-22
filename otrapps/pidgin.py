#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''a module for reading and writing Pidgin's OTR key data'''

from __future__ import print_function
import os
import sys
from bs4 import BeautifulSoup

if __name__ == '__main__':
    sys.path.insert(0, "../") # so the main() test suite can find otrapps module
import otrapps.util
from otrapps.otr_private_key import OtrPrivateKeys
from otrapps.otr_fingerprints import OtrFingerprints

class PidginProperties():

    if sys.platform == 'win32':
        path = os.path.join(os.environ.get('APPDATA'), '.purple')
    else:
        path = os.path.expanduser('~/.purple')
    accountsfile = 'accounts.xml'
    keyfile = 'otr.private_key'
    fingerprintfile = 'otr.fingerprints'

    @staticmethod
    def _get_resources(settingsdir):
        '''parse out the XMPP Resource from every Pidgin account'''
        resources = dict()
        accountsfile = os.path.join(settingsdir, PidginProperties.accountsfile)
        if not os.path.exists(accountsfile):
            print('Pidgin WARNING: No usable accounts.xml file found, add XMPP Resource to otr.private_key by hand!')
            return resources
        xml = ''
        for line in open(accountsfile, 'r').readlines():
            xml += line
        for e in BeautifulSoup(xml)(text='prpl-jabber'):
            pidginname = e.parent.parent.find('name').contents[0].split('/')
            name = pidginname[0]
            if len(pidginname) == 2:
                resources[name] = pidginname[1]
            else:
                # Pidgin requires an XMPP Resource, even if its blank
                resources[name] = ''
        return resources

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = PidginProperties.path

        kf = os.path.join(settingsdir, PidginProperties.keyfile)
        if os.path.exists(kf):
            keydict = OtrPrivateKeys.parse(kf)
        else:
            keydict = dict()

        fpf = os.path.join(settingsdir, PidginProperties.fingerprintfile)
        if os.path.exists(fpf):
            otrapps.util.merge_keydicts(keydict, OtrFingerprints.parse(fpf))

        resources = PidginProperties._get_resources(settingsdir)
        for name, key in keydict.items():
            if key['protocol'] == 'prpl-jabber' \
                    and 'x' in key.keys() \
                    and name in resources.keys():
                key['resource'] = resources[name]

        return keydict

    @staticmethod
    def write(keydict, savedir):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')

        kf = os.path.join(savedir, PidginProperties.keyfile)
        # Pidgin requires the XMPP resource in the account name field of the
        # OTR private keys file, so fetch it from the existing account info
        if os.path.exists(os.path.join(savedir, PidginProperties.accountsfile)):
            accountsdir = savedir
        elif os.path.exists(os.path.join(PidginProperties.path,
                                         PidginProperties.accountsfile)):
            accountsdir = PidginProperties.path
        else:
            raise Exception('Cannot find "' + PidginProperties.accountsfile
                            + '" in "' + savedir + '"')
        resources = PidginProperties._get_resources(accountsdir)
        OtrPrivateKeys.write(keydict, kf, resources=resources)

        accounts = []
        # look for all private keys and use them for the accounts list
        for name, key in keydict.items():
            if 'x' in key:
                accounts.append(name)
        fpf = os.path.join(savedir, PidginProperties.fingerprintfile)
        OtrFingerprints.write(keydict, fpf, accounts, resources=resources)


if __name__ == '__main__':

    import pprint
    import shutil

    print('Pidgin stores its files in ' + PidginProperties.path)

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/pidgin'

    keydict = PidginProperties.parse(settingsdir)
    pprint.pprint(keydict)

    if not os.path.exists(os.path.join('/tmp', PidginProperties.accountsfile)):
        shutil.copy(os.path.join(settingsdir, PidginProperties.accountsfile),
                    '/tmp')
    PidginProperties.write(keydict, '/tmp')
