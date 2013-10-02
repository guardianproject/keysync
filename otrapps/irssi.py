#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import platform
import sys
import plistlib
import util

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

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
            util.merge_keydicts(keydict, OtrFingerprints.parse(fpf))

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
