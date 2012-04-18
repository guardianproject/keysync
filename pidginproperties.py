#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import platform
import plistlib

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

class PidginProperties():

    if platform.system() == 'Windows':
        path = os.path.expanduser('~/Application Data/.purple')
    else:
        path = os.path.expanduser('~/.purple')

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = PidginProperties.path
        keys = OtrPrivateKeys.parse(os.path.join(settingsdir, 'otr.private_key'))
        keys += OtrFingerprints.parse(os.path.join(settingsdir, 'otr.fingerprints'))
        return keys

    @staticmethod
    def write(keys, savedir):
        pass

if __name__ == '__main__':

    import pprint

    print 'Pidgin stores its files in ' + PidginProperties.path

    l = PidginProperties.parse('tests/pidgin')
    pprint.pprint(l)
