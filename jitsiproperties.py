#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import re
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
    def parse(filename):
        # TODO switch this to settingsdir like the others
        p = Properties()
        p.load(open(filename))
        ret = []
        for item in p.items():
            propkey = item[0]
            if re.match('net\.java\.sip\.communicator\.impl\.protocol\.jabber\.acc[0-9]+\.ACCOUNT_UID', propkey):
                keydict = {}
                keydict['protocol'] = 'prpl-jabber'
                keydict['name'] = JitsiProperties._parse_account_uid(item[1])

                propkey_base = ('net.java.sip.communicator.plugin.otr.'
                                + re.sub('[^a-zA-Z0-9_]', '_', item[1]))
                keydict['private-key'] = p.getProperty(propkey_base + '_privateKey')
                keydict['public_key'] = p.getProperty(propkey_base + '_publicKey')
                ret.append(keydict)
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey.verified', propkey)):
                print propkey
                keydict = {}
                keydict['name'] = '.'.join(propkey.split('.')[-1].split('_')[0:-1])
                keydict['verification'] = 'verified'
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey', propkey) and not
                  re.match('net\.java\.sip\.communicator\.plugin\.otr\.(Jabber_|Google_Talk_)', propkey)):
                keydict = {}
                keydict['name'] = '.'.join(propkey.split('.')[-1].split('_')[0:-1])
                keydict['public-key'] = item[1]
                ret.append(keydict)
        return ret



#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):

    print 'Jitsi stores its files in ' + JitsiProperties.path

    p = JitsiProperties.parse('tests/jitsi/sip-communicator.properties')
    print '----------------------------------------'
    for item in p:
        print item
    print '----------------------------------------'

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])


