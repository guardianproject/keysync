#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import pyjavaproperties
import util

# TODO parse private keys

class GibberbotProperties():

    @staticmethod
    def parse(filename):
        '''parse the given file into the standard keydict'''
        p = pyjavaproperties.Properties()
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
                ret.append(('private-key', id,
                            util.ParsePkcs8(item[1].replace('\\n', ''))))
        return ret

    @staticmethod
    def write(keys, savedir):
        '''given a list of keydicts, generate a gibberbot file'''
        p = pyjavaproperties.Properties()
        for key in keys:
            if 'x' in key:
                p.setProperty(key['name'] + '.publicKey', util.ExportDsaX509(key))
            if 'y' in key:
                p.setProperty(key['name'] + '.privateKey', util.ExportDsaPkcs8(key))
            if 'verification' in key and key['verification'] != None:
                p.setProperty(key['name'] + '.' + key['fingerprint'] + '.publicKey.verified',
                              'true')
        f = open(os.path.join(savedir, 'otr_keystore'), 'w')
        p.store(f)

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


