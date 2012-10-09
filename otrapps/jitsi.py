#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import re
import sys
from pyjavaproperties import Properties
import util

# the accounts, private/public keys, and fingerprints are in sip-communicator.properties
# the contacts list is in contactlist.xml

class JitsiProperties():

    if platform.system() == 'Darwin':
        path = os.path.expanduser('~/Library/Application Support/Jitsi')
    elif platform.system() == 'Windows':
        path = os.path.expanduser('~/Application Data/Jitsi')
    else:
        path = os.path.expanduser('~/.jitsi')

    @staticmethod
    def _parse_account_uid(uidstring):
        username, domain, server = uidstring.split(':')[1].split('@')
        return username + '@' + domain

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = JitsiProperties.path
        p = Properties()
        p.load(open(os.path.join(settingsdir, 'sip-communicator.properties')))
        ret = []
        for item in p.items():
            propkey = item[0]
            if re.match('net\.java\.sip\.communicator\.impl\.protocol\.jabber\.acc[0-9]+\.ACCOUNT_UID', propkey):
                keydict = {}
                keydict['protocol'] = 'prpl-jabber'
                keydict['name'] = JitsiProperties._parse_account_uid(item[1])

                propkey_base = ('net.java.sip.communicator.plugin.otr.'
                                + re.sub('[^a-zA-Z0-9_]', '_', item[1]))
                private_key = p.getProperty(propkey_base + '_privateKey').strip()
                public_key = p.getProperty(propkey_base + '_publicKey').strip()
                numdict = util.ParsePkcs8(private_key)
                keydict['x'] = numdict['x']
                numdict = util.ParseX509(public_key)
                for num in ('y', 'g', 'p', 'q'):
                    keydict[num] = numdict[num]
                keydict['fingerprint'] = util.fingerprint((keydict['y'], keydict['g'], keydict['p'], keydict['q']))
                verifiedkey = ('net.java.sip.communicator.plugin.otr.'
                               + re.sub('[^a-zA-Z0-9_]', '_', keydict['name'])
                               + '_publicKey_verified')
                if p.getProperty(verifiedkey).strip() == 'true':
                    keydict['verification'] = 'verified'
                ret.append(keydict)
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey.verified', propkey)):
                keydict = {}
                keydict['name'] = '.'.join(propkey.split('.')[-1].split('_')[0:-1])
                keydict['verification'] = 'verified'
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey', propkey) and not
                  re.match('net\.java\.sip\.communicator\.plugin\.otr\.(Jabber_|Google_Talk_)', propkey)):
                keydict = {}
                keydict['protocol'] = 'prpl-jabber'
                keydict['name'] = '.'.join(propkey.split('.')[-1].split('_')[0:-1])
                numdict = util.ParseX509(item[1])
                for num in ('y', 'g', 'p', 'q'):
                    keydict[num] = numdict[num]
                keydict['fingerprint'] = util.fingerprint((keydict['y'], keydict['g'], keydict['p'], keydict['q']))
                ret.append(keydict)
        return ret


#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):

    print 'Jitsi stores its files in ' + JitsiProperties.path

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/jitsi'

    p = JitsiProperties.parse(settingsdir)
    print '----------------------------------------'
    for item in p:
        print item
    print '----------------------------------------'

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])


