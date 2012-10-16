#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import re
import sys
from pyjavaproperties import Properties
from BeautifulSoup import BeautifulSoup
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
    propertiesfile = 'sip-communicator.properties'
    contactsfile = 'contactlist.xml'

    @staticmethod
    def _parse_account_uid(uidstring):
        username, domain, server = uidstring.split(':')[1].split('@')
        return username + '@' + domain


    @staticmethod
    def _parse_account_from_propkey(settingsdir, propkey):
        '''give a Java Properties key, parse out a real account UID, based on
        what's listed in the contacts file'''
        # jitsi stores the account name in the properties key, so it strips the @ out
        m = re.match('net\.java\.sip\.communicator\.plugin\.otr\.(.*)_publicKey.*', propkey)
        name_from_prop = '.'.join(m.group(1).split('_'))
        # so let's find where the @ was originally placed:
        xml = ''
        for line in open(os.path.join(settingsdir, JitsiProperties.contactsfile), 'r').readlines():
            xml += line
        name = None
        for e in BeautifulSoup(xml).findAll('contact'):
            if re.match(name_from_prop, e['address']):
                name = e['address']
                break
        return str(name)


    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = JitsiProperties.path
        p = Properties()
        p.load(open(os.path.join(settingsdir, JitsiProperties.propertiesfile)))
        keydict = dict()
        for item in p.items():
            propkey = item[0]
            name = ''
            if re.match('net\.java\.sip\.communicator\.impl\.protocol\.jabber\.acc[0-9]+\.ACCOUNT_UID', propkey):
                name = JitsiProperties._parse_account_uid(item[1])
                if name in keydict:
                    key = keydict[name]
                else:
                    key = dict()
                    key['name'] = name
                    key['protocol'] = 'prpl-jabber'
                    keydict[name] = key

                propkey_base = ('net.java.sip.communicator.plugin.otr.'
                                + re.sub('[^a-zA-Z0-9_]', '_', item[1]))
                private_key = p.getProperty(propkey_base + '_privateKey').strip()
                public_key = p.getProperty(propkey_base + '_publicKey').strip()
                numdict = util.ParsePkcs8(private_key)
                key['x'] = numdict['x']
                numdict = util.ParseX509(public_key)
                for num in ('y', 'g', 'p', 'q'):
                    key[num] = numdict[num]
                key['fingerprint'] = util.fingerprint((key['y'], key['g'], key['p'], key['q']))
                verifiedkey = ('net.java.sip.communicator.plugin.otr.'
                               + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                               + '_publicKey_verified')
                if p.getProperty(verifiedkey).strip() == 'true':
                    key['verification'] = 'verified'
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey_verified', propkey)):
                name = JitsiProperties._parse_account_from_propkey(settingsdir, propkey)
                if name != None:
                    if name not in keydict:
                        key = dict()
                        key['name'] = name
                        keydict[name] = key
                    keydict[name]['verification'] = 'verified'
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey', propkey) and not
                  re.match('net\.java\.sip\.communicator\.plugin\.otr\.(Jabber_|Google_Talk_)', propkey)):
                name = JitsiProperties._parse_account_from_propkey(settingsdir, propkey)
                if name not in keydict:
                    key = dict()
                    key['name'] = name
                    key['protocol'] = 'prpl-jabber'
                    keydict[name] = key
                numdict = util.ParseX509(item[1])
                for num in ('y', 'g', 'p', 'q'):
                    key[num] = numdict[num]
                key['fingerprint'] = util.fingerprint((key['y'], key['g'], key['p'], key['q']))
        return keydict

    @staticmethod
    def write(keydict, savedir):
        pass


#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):
    import pprint

    print 'Jitsi stores its files in ' + JitsiProperties.path

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/jitsi'

    p = JitsiProperties.parse(settingsdir)
    print '----------------------------------------'
    pprint.pprint(p)
    print '----------------------------------------'

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
