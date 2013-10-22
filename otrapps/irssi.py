#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''a module for reading and writing irssi's OTR key data'''

from __future__ import print_function
import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, "../") # so the main() test suite can find otrapps module
import otrapps.util
from otrapps.otr_private_key import OtrPrivateKeys
from otrapps.otr_fingerprints import OtrFingerprints

class IrssiProperties():

    path = os.path.expanduser('~/.irssi/otr')
    keyfile = 'otr.key'
    fingerprintfile = 'otr.fp'
    files = (keyfile, fingerprintfile)

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = IrssiProperties.path

        kf = os.path.join(settingsdir, IrssiProperties.keyfile)
        if os.path.exists(kf):
            keydict = OtrPrivateKeys.parse(kf)
        else:
            keydict = dict()

        fpf = os.path.join(settingsdir, IrssiProperties.fingerprintfile)
        if os.path.exists(fpf):
            otrapps.util.merge_keydicts(keydict, OtrFingerprints.parse(fpf))

        return keydict

    @staticmethod
    def write(keydict, savedir):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')

        kf = os.path.join(savedir, IrssiProperties.keyfile)
        OtrPrivateKeys.write(keydict, kf)

        accounts = []
        # look for all private keys and use them for the accounts list
        for name, key in keydict.items():
            if 'x' in key:
                accounts.append(name)
        fpf = os.path.join(savedir, IrssiProperties.fingerprintfile)
        OtrFingerprints.write(keydict, fpf, accounts)


if __name__ == '__main__':

    import pprint

    print('Irssi stores its files in ' + IrssiProperties.path)

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/irssi'

    keydict = IrssiProperties.parse(settingsdir)
    pprint.pprint(keydict)

    IrssiProperties.write(keydict, '/tmp')
