#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import platform
import sys
import plistlib

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

class IrssiProperties():

    path = os.path.expanduser('~/.irssi/otr')

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = IrssiProperties.path
        keys = OtrPrivateKeys.parse(os.path.join(settingsdir, 'otr.key'))
        keys += OtrFingerprints.parse(os.path.join(settingsdir, 'otr.fp'))
        return keys

    @staticmethod
    def write(keys, savedir):
        pass

if __name__ == '__main__':

    import pprint

    print 'Irssi stores its files in ' + IrssiProperties.path

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = 'tests/irssi'

    l = IrssiProperties.parse(settingsdir)
    pprint.pprint(l)
