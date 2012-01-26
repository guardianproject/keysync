#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import pyjavaproperties
import util

# TODO parse public keys into fingerprints

class GibberbotProperties():

    @staticmethod
    def parse(filename):
        '''parse the given file into the standard keydict'''
        p = pyjavaproperties.Properties()
        p.load(open(filename))
        parsed = []
        for item in p.items():
            keydata = item[0]
            if keydata.endswith('.publicKey'):
                id = '.'.join(keydata.split('.')[0:-1])
                parsed.append(('public-key', id, item[1]))
            if keydata.endswith('.publicKey.verified'):
                keylist = keydata.split('.')
                fingerprint = keylist[-3]
                id = '.'.join(keylist[0:-3])
                parsed.append(('verified', id, fingerprint))
            if keydata.endswith('.privateKey'):
                id = '.'.join(keydata.split('.')[0:-1])
                parsed.append(('private-key', id, item[1]))
        # create blank keys for all IDs
        keydict = dict()
        for keydata in parsed:
            name = keydata[1]
            if not name in keydict:
                keydict[name] = dict()
                keydict[name]['name'] = name
                keydict[name]['protocol'] = 'prpl-jabber'
            if keydata[0] == 'private-key':
                #print 'private-key: ' + name + ' | ',
                cleaned = keydata[2].replace('\\n', '')
                numdict = util.ParsePkcs8(cleaned)
                for num in ('q', 'p', 'g', 'x'):
                    keydict[name][num] = numdict[num]
            elif keydata[0] == 'verified':
                keydict[name]['verification'] = 'verified'
                keydict[name]['fingerprint'] = keydata[2]
            elif keydata[0] == 'public-key':
                #print 'public-key: ' + name + ' | ',
                cleaned = keydata[2].replace('\\n', '')
                numdict = util.ParseX509(cleaned)
                for num in ('q', 'p', 'g', 'y'):
                    keydict[name][num] = numdict[num]
                keydict[name]['fingerprint'] = 'PLACEHOLDER'
                #dsakey = DSAKey(keytuple)
                #keydict['fingerprint'] = dsakey.cfingerprint()
        return keydict.values()

    @staticmethod
    def write(keys, savedir):
        '''given a list of keydicts, generate a gibberbot file'''
        p = pyjavaproperties.Properties()
        for key in keys:
            if 'y' in key:
                p.setProperty(key['name'] + '.publicKey', util.ExportDsaX509(key))
            if 'x' in key:
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


