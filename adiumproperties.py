#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import plistlib

from otr_private_key import OtrPrivateKeys
from otr_fingerprints import OtrFingerprints

class AdiumProperties():

    @staticmethod
    def parse(settingsdir):
        keys = OtrPrivateKeys.parse(os.path.join(settingsdir, 'otr.private_key'))
        keys += OtrFingerprints.parse(os.path.join(settingsdir, 'otr.fingerprints'))
        accounts = plistlib.readPlist(os.path.join(settingsdir, 'Accounts.plist'))['Accounts']
        for key in keys:
            for account in accounts:
                if account['ObjectID'] == key['name']:
                    key['name'] = account['UID']
        return keys


if __name__ == '__main__':

    import pprint

    l = AdiumProperties.parse('tests/adium')
    pprint.pprint(l)
