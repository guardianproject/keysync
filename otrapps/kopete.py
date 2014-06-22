#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''a module for reading and writing Kopete's OTR key data'''

from __future__ import print_function
import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, "../") # so the main() test suite can find otrapps module
import otrapps.util
from otrapps.otr_private_key import OtrPrivateKeys
from otrapps.otr_fingerprints import OtrFingerprints

class KopeteProperties():

    path = os.path.expanduser('~/.kde/share/apps/kopete_otr')
    keyfile = 'privkeys'
    fingerprintfile = 'fingerprints'
    files = (keyfile, fingerprintfile)

    @staticmethod
    def _convert_protocol_name(protocol):
        if protocol == 'Jabber':
            return 'prpl-jabber'
        elif protocol == 'prpl-jabber':
            return 'Jabber'
        elif protocol == 'Google Talk':
            # this should also mark it as the gtalk variant
            return 'prpl-jabber'
        else:
            print('IMPLEMENTME')
            print(protocol)
            return 'IMPLEMENTME'

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = KopeteProperties.path

        kf = os.path.join(settingsdir, KopeteProperties.keyfile)
        if os.path.exists(kf):
            keydict = OtrPrivateKeys.parse(kf)
            for key in keydict:
                for value in keydict[key]:
                    if value == 'protocol':
                        keydict[key][value] = KopeteProperties._convert_protocol_name(keydict[key][value])
        else:
            keydict = dict()

        fpf = os.path.join(settingsdir, KopeteProperties.fingerprintfile)
        if os.path.exists(fpf):
            tmpdict = OtrFingerprints.parse(fpf)
            for key in tmpdict:
                for value in tmpdict[key]:
                    if value == 'protocol':
                        tmpdict[key][value] = KopeteProperties._convert_protocol_name(tmpdict[key][value])

            otrapps.util.merge_keydicts(keydict, tmpdict)

        return keydict

    @staticmethod
    def write(keydict, savedir):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')

        for key in keydict:
            for value in keydict[key]:
                if value == 'protocol':
                    keydict[key][value] = KopeteProperties._convert_protocol_name(keydict[key][value])

        kf = os.path.join(savedir, KopeteProperties.keyfile)
        OtrPrivateKeys.write(keydict, kf)

        accounts = []
        # look for all private keys and use them for the accounts list
        for name, key in keydict.items():
            if 'x' in key:
                accounts.append(name)
        fpf = os.path.join(savedir, KopeteProperties.fingerprintfile)
        OtrFingerprints.write(keydict, fpf, accounts)



if __name__ == '__main__':

    import pprint

    print('Kopete stores its files in ' + KopeteProperties.path)

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/kopete'

    keydict = KopeteProperties.parse(settingsdir)
    pprint.pprint(keydict)

    KopeteProperties.write(keydict, '/tmp')
