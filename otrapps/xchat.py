#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import platform
import sys
import plistlib
import util

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

class XchatProperties():

    path = os.path.expanduser('~/.xchat2/otr')
    keyfile = 'otr.key'
    fingerprintfile = 'otr.fp'

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = XchatProperties.path

        kf = os.path.join(settingsdir, XchatProperties.keyfile)
        if os.path.exists(kf):
            keydict = OtrPrivateKeys.parse(kf)
        else:
            keydict = dict()

        fpf = os.path.join(settingsdir, XchatProperties.fingerprintfile)
        if os.path.exists(fpf):
            util.merge_keydicts(keydict, OtrFingerprints.parse(fpf))

        return keydict

    @staticmethod
    def write(keydict, savedir):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')

        kf = os.path.join(savedir, XchatProperties.keyfile)
        OtrPrivateKeys.write(keydict, kf)

        accounts = []
        # look for all private keys and use them for the accounts list
        for name, key in keydict.iteritems():
            if 'x' in key:
                accounts.append(name)
        fpf = os.path.join(savedir, XchatProperties.fingerprintfile)
        OtrFingerprints.write(keydict, fpf, accounts)



if __name__ == '__main__':

    import pprint

    print 'Xchat stores its files in ' + XchatProperties.path

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/xchat'

    keydict = XchatProperties.parse(settingsdir)
    pprint.pprint(keydict)

    XchatProperties.write(keydict, '/tmp')
