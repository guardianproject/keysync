#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''a module for reading and writing Gajim's OTR key data'''

from __future__ import print_function
import os
import glob
import platform
import sys
import re
import collections

import potr

if __name__ == '__main__':
    sys.path.insert(0, "../")  # so the main() test suite can find otrapps module

import otrapps.util
from otrapps.otr_fingerprints import OtrFingerprints

# the private key is stored in ~/.local/share/gajim/_SERVERNAME_.key_file
# the fingerprints are stored in ~/.local/share/gajim/_SERVERNAME_.fpr
# the accounts are stored in ~/.config/gajim/config


class GajimProperties():

    if platform.system() == 'Windows':
        path = os.path.expanduser('~/Application Data/Gajim')
        accounts_path = '???'
    else:
        path = os.path.expanduser('~/.local/share/gajim')
        accounts_path = os.path.expanduser('~/.config/gajim')

    @staticmethod
    def _parse_account_config(accounts_path):
        """
        Crudely parses the dot-style config syntax of gajim's config file
        """
        if accounts_path is None:
            accounts_path = GajimProperties.accounts_path

        accounts_config = os.path.join(accounts_path, 'config')

        keys = ['name', 'hostname', 'resource']
        patterns = []
        for key in keys:
            # matches lines like:
            #  accounts.guardianproject.info.hostname = "guardianproject.info"
            patterns.append((key, re.compile('accounts\.(.*)\.%s = (.*)' % key)))

        accounts = collections.defaultdict(dict)
        for line in open(accounts_config, 'r'):
            for key, pattern in patterns:
                for match in re.finditer(pattern, line):
                    accounts[match.groups()[0]][key] = match.groups()[1]

        return accounts

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir is None:
            settingsdir = GajimProperties.path
            accounts_config = GajimProperties.accounts_path
        else:
            accounts_config = settingsdir

        keydict = dict()
        for fpf in glob.glob(os.path.join(settingsdir, '*.fpr')):
            print('Reading in ' + fpf)
            keys = OtrFingerprints.parse(fpf)

            # replace gajim's 'xmpp' protocol with 'prpl-jabber' that we use in keysync
            for key, value in keys.items():
                value['protocol'] = 'prpl-jabber'
                keys[key] = value

            otrapps.util.merge_keydicts(keydict, keys)

        accounts = GajimProperties._parse_account_config(accounts_config)

        for key_file in glob.glob(os.path.join(settingsdir, '*.key3')):
            account_name = os.path.splitext(os.path.basename(key_file))[0]
            if not account_name in accounts.keys():
                print("ERROR found %s not in the account list", key_file)
                continue
            with open(key_file, 'rb') as key_file:
                name = '%s@%s' % (accounts[account_name]['name'],
                                  accounts[account_name]['hostname'])
                if name in keydict:
                    key = keydict[name]
                else:
                    key = dict()
                    key['name'] = name
                key['protocol'] = 'prpl-jabber'
                key['resource'] = accounts[account_name]['resource']

                pk = potr.crypt.PK.parsePrivateKey(key_file.read())[0]
                keydata = ['y', 'g', 'p', 'q', 'x']
                for data in keydata:
                    key[data] = getattr(pk.priv, data)

                key['fingerprint'] = otrapps.util.fingerprint((key['y'], key['g'],
                                                               key['p'], key['q']))

                keydict[key['name']] = key

        return keydict

    @staticmethod
    def write(keys, savedir):
        if not os.path.exists(savedir):
            raise Exception('"' + savedir + '" does not exist!')


#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):
    import pprint

    print('Gajim stores its files in ' + GajimProperties.path)

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/gajim'

    keydict = GajimProperties.parse(settingsdir)
    print('----------------------------------------')
    pprint.pprint(keydict)
    print('----------------------------------------')
    GajimProperties.write(keydict, '/tmp')

if __name__ == "__main__":
    main(sys.argv[1:])
