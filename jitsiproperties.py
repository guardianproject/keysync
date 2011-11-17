#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from pyjavaproperties import Properties
import re

# the accounts, private/public keys, and fingerprints are in sip-communicator.properties
# the contacts list is in contactlist.xml

class JitsiProperties():

    @staticmethod
    def _parse_account_uid(uidstring):
        username, domain, server = uidstring.split(':')[1].split('@')
        return username + '@' + domain

    @staticmethod
    def parse(filename):
        p = Properties()
        p.load(open(filename))
        ret = []
        for item in p.items():
            key = item[0]
            if re.match('net\.java\.sip\.communicator\.impl\.protocol\.jabber\.acc[0-9]+\.ACCOUNT_UID', key):
                id = JitsiProperties._parse_account_uid(item[1])
                prop_key = ('net.java.sip.communicator.plugin.otr.'
                            + re.sub('[^a-zA-Z0-9_]', '_', item[1]))

                private_key_prop_key = prop_key + '_privateKey'
                private_key = p.getProperty(private_key_prop_key)
                ret.append(('private-key', id, 'prpl-jabber', private_key))

                public_key_prop_key = prop_key + '_publicKey'
                public_key = p.getProperty(public_key_prop_key)
                ret.append(('public-key', id, 'prpl-jabber', public_key))
            elif (re.match('net\.java\.sip\.communicator\.plugin\.otr\..*_publicKey', key) and not
                  re.match('net\.java\.sip\.communicator\.plugin\.otr\.(Jabber_|Google_Talk_)', key)):
                prop = '.'.join(key.split('.')[-1].split('_')[0:-1])
                ret.append(('fingerprint', prop, item[1]))
        return ret



#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):
    p = JitsiProperties.parse('tests/jitsi/sip-communicator.properties')
    print '----------------------------------------'
    for item in p:
        print item
    print '----------------------------------------'

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])


