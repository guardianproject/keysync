#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''a module for reading and writing Jitsi's OTR key data'''

from __future__ import print_function
import os
import platform
import re
import sys
from pyjavaproperties import Properties
from bs4 import BeautifulSoup

if __name__ == '__main__':
    sys.path.insert(0, "../") # so the main() test suite can find otrapps module
import otrapps.util


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
    files = (propertiesfile, contactsfile)

    @staticmethod
    def _parse_account_uid(uidstring):
        username, domain, server = uidstring.split(':')[1].split('@')
        return username + '@' + domain

    @staticmethod
    def _convert_protocol_name(protocol):
        if protocol == 'Jabber':
            return 'prpl-jabber'
        elif protocol == 'Google Talk':
            # this should also mark it as the gtalk variant
            return 'prpl-jabber'
        else:
            return 'IMPLEMENTME'

    @staticmethod
    def _parse_account_from_propkey(settingsdir, propkey):
        '''give a Java Properties key, parse out a real account UID and
        protocol, based on what's listed in the contacts file'''
        # jitsi stores the account name in the properties key, so it strips the @ out
        m = re.match('net\.java\.sip\.communicator\.plugin\.otr\.(.*)_publicKey.*', propkey)
        name_from_prop = '.'.join(m.group(1).split('_'))
        # so let's find where the @ was originally placed:
        xml = ''
        for line in open(os.path.join(settingsdir, JitsiProperties.contactsfile), 'r').readlines():
            xml += line
        name = None
        protocol = None
        for e in BeautifulSoup(xml).find_all('contact'):
            if re.match(name_from_prop, e['address']):
                name = e['address']
                protocol = JitsiProperties._convert_protocol_name(e['account-id'].split(':')[0])
                break
        return str(name), protocol


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
                numdict = otrapps.util.ParsePkcs8(private_key)
                key['x'] = numdict['x']
                numdict = otrapps.util.ParseX509(public_key)
                for num in ('y', 'g', 'p', 'q'):
                    key[num] = numdict[num]
                key['fingerprint'] = otrapps.util.fingerprint((key['y'], key['g'], key['p'], key['q']))
                verifiedkey = ('net.java.sip.communicator.plugin.otr.'
                               + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                               + '_publicKey_verified')
                if p.getProperty(verifiedkey).strip() == 'true':
                    key['verification'] = 'verified'
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey_verified', propkey)):
                name, protocol = JitsiProperties._parse_account_from_propkey(settingsdir, propkey)
                if name != None:
                    if name in keydict:
                        key = keydict[name]
                    else:
                        key = dict()
                        key['name'] = name
                        keydict[name] = key
                    if protocol and 'protocol' not in keydict[name]:
                        key['protocol'] = protocol
                    key['verification'] = 'verified'
            # if the protocol name is included in the property name, its a local account with private key
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey', propkey) and not
                  re.match('net\.java\.sip\.communicator\.plugin\.otr\.(Jabber_|Google_Talk_)', propkey)):
                name, ignored = JitsiProperties._parse_account_from_propkey(settingsdir, propkey)
                if name in keydict:
                    key = keydict[name]
                else:
                    key = dict()
                    key['name'] = name
                    key['protocol'] = 'prpl-jabber'
                    keydict[name] = key
                numdict = otrapps.util.ParseX509(item[1])
                for num in ('y', 'g', 'p', 'q'):
                    key[num] = numdict[num]
                key['fingerprint'] = otrapps.util.fingerprint((key['y'], key['g'], key['p'], key['q']))
        return keydict

    @staticmethod
    def write(keydict, savedir):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')

        loadfile = os.path.join(savedir, JitsiProperties.propertiesfile)
        savefile = loadfile
        if not os.path.exists(loadfile) and os.path.exists(JitsiProperties.path):
            print('Jitsi NOTICE: "' + loadfile + '" does not exist! Reading from:')
            loadfile = os.path.join(JitsiProperties.path, JitsiProperties.propertiesfile)
            print('\t"' + loadfile + '"')

        propkey_base = 'net.java.sip.communicator.plugin.otr.'
        p = Properties()
        p.load(open(loadfile))
        for name, key in keydict.items():
            if 'verification' in key and key['verification'] != '':
                verifiedkey = (propkey_base + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                               + '_publicKey_verified')
                p[verifiedkey] = 'true'
            if 'y' in key:
                pubkey = (propkey_base + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                          + '_publicKey')
                p.setProperty(pubkey, otrapps.util.ExportDsaX509(key))
            if 'x' in key:
                protocol_id = 'UNKNOWN_'
                domain_id = 'unknown'
                servername = None
                if '@' in key['name']:
                    domainname = key['name'].split('@')[1]
                    domain_id = re.sub('[^a-zA-Z0-9_]', '_', domainname)
                    if domainname == 'chat.facebook.com':
                        protocol_id = 'Facebook_'
                    elif domainname == 'gmail.com' \
                            or domainname == 'google.com' \
                            or domainname == 'googlemail.com':
                        protocol_id = 'Google_Talk_'
                        servername = 'talk_google_com'
                    else:
                        protocol_id = 'Jabber_'
                else:
                    if key['protocol'] == 'prpl-icq':
                        protocol_id = 'ICQ_'
                        domain_id = 'icq_com'
                    elif key['protocol'] == 'prpl-yahoo':
                        protocol_id = 'Yahoo__'
                        domain_id = 'yahoo_com'
                # Writing
                pubkey = (propkey_base + protocol_id + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                          + '_' + domain_id + '_publicKey')
                p.setProperty(pubkey, otrapps.util.ExportDsaX509(key))
                privkey = (propkey_base + protocol_id + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                           + '_' + domain_id + '_privateKey')
                p.setProperty(privkey, otrapps.util.ExportDsaPkcs8(key))
		   
                if servername:
                    pubkey = (propkey_base + protocol_id + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                              + '_' + servername + '_publicKey')
                    p.setProperty(pubkey, otrapps.util.ExportDsaX509(key))
                    privkey = (propkey_base + protocol_id + re.sub('[^a-zA-Z0-9_]', '_', key['name'])
                               + '_' + servername + '_privateKey')
                    p.setProperty(privkey, otrapps.util.ExportDsaPkcs8(key))
		   		
        p.store(open(savefile, 'w'))



#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):
    import pprint

    print('Jitsi stores its files in ' + JitsiProperties.path)

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/jitsi'

    p = JitsiProperties.parse(settingsdir)
    print('----------------------------------------')
    pprint.pprint(p)
    print('----------------------------------------')

if __name__ == "__main__":
    main(sys.argv[1:])
