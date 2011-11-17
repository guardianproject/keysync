#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from pyjavaproperties import Properties

class GibberbotProperties():

    @staticmethod
    def parse(filename):
        p = Properties()
        p.load(open(filename))
        ret = []
        for item in p.items():
            key = item[0]
            if key.endswith('.publicKey'):
                id = '.'.join(key.split('.')[0:-1])
                ret.append(('public-key', id, item[1]))
            if key.endswith('.publicKey.verified'):
                keylist = key.split('.')
                fingerprint = keylist[-3]
                id = '.'.join(keylist[0:-3])
                ret.append(('verified', id, fingerprint))
            if key.endswith('.privateKey'):
                id = '.'.join(key.split('.')[0:-1])
                ret.append(('private-key', id, item[1]))
        return ret



#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):
    p = GibberbotProperties.parse('tests/gibberbot/otr_keystore')
    print '----------------------------------------'
    for item in p:
        print item
    print '----------------------------------------'

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])


