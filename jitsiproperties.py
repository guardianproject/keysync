#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from pyjavaproperties import Properties
import re

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
#            print "item: ",
#            print item
            if re.match('net\.java\.sip\.communicator\.impl\.protocol\.jabber\.acc[0-9]+\.ACCOUNT_UID',
                        item[0]):
                id = JitsiProperties._parse_account_uid(item[1])
                private_key_prop_key = ('net.java.sip.communicator.plugin.otr.'
                                        + re.sub('[^a-zA-Z0-9_]', '_', item[1])
                                        + '_privateKey')
                private_key = p.getProperty(private_key_prop_key)
                ret.append(('private-key', id, 'prpl-jabber', private_key))
            
            if item[0].startswith('net.java.sip.communicator.plugin.otr.'):
                prop = item[0].split('.')[-1]
                if prop.endswith('privateKey'):
                    m = re.match('(.*)_privateKey', prop)
                    ret.append(('private-key', m.group(1), item[1]))
                print prop
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


