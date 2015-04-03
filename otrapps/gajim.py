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
import shutil

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
        accounts_file = 'config'
        path = os.path.expanduser('~/.local/share/gajim')
        accounts_path = os.path.expanduser('~/.config/gajim')

    @staticmethod
    def _parse_account_config(accounts_path):
        """
        Crudely parses the dot-style config syntax of gajim's config file
        """
        if accounts_path is None:
            accounts_path = GajimProperties.accounts_path

        accounts_config = os.path.join(accounts_path, GajimProperties.accounts_file)

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
        
        # get existing accounts, we need that to figure out how to call the keys
        if os.path.exists(os.path.join(savedir, GajimProperties.accounts_file)):
            accountsdir = savedir
        elif os.path.exists(os.path.join(GajimProperties.accounts_path,
                                         GajimProperties.accounts_file)):
            accountsdir = GajimProperties.accounts_path
        else:
            raise Exception('Cannot find "' + GajimProperties.accounts_file
                            + '" in "' + savedir + '"')
        accounts = GajimProperties._parse_account_config(accountsdir)
        
        # now for each account, write the fingerprints and key
        accounts_written = set()
        for account_name in accounts:
            xmpp_name = accounts[account_name]['name'] + '@' + accounts[account_name]['hostname']
            if not xmpp_name in keys:
                # no private key for this account, skip it
                continue
            key = keys[xmpp_name]
            if not 'x' in key:
                # this is not a private key, nothing to do here
                continue
            
            # write fingerprints. We do this ourselves to make sure we get the right line-endings.
            with open(os.path.join(savedir, account_name + '.fpr'), 'w') as fp_file:
                for fp_name, fp_key in keys.items():
                    if 'fingerprint' in fp_key and 'verification' in fp_key:
                        row = [fp_name, xmpp_name, 'xmpp', fp_key['fingerprint'], fp_key['verification']]
                        fp_file.write('\t'.join(row)+'\n')
            
            # write private key
            private_key = potr.compatcrypto.DSAKey((key['y'], key['g'], key['p'], key['q'], key['x']), private=True)
            with open(os.path.join(savedir, account_name + '.key3'), 'wb') as key_file:
                key_file.write(private_key.serializePrivateKey())
            
            print("Wrote key for Gajim:",xmpp_name)
            accounts_written.add(xmpp_name)
        
        # check for unwritten keys
        for key_name in keys.keys():
            if 'x' in keys[key_name]:
                if key_name not in accounts_written:
                    print("No Gajim accont found for",key_name+", key has not been written.")


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
    if not os.path.exists(os.path.join('/tmp', GajimProperties.accounts_file)):
        shutil.copy(os.path.join(settingsdir, GajimProperties.accounts_file), '/tmp')
    GajimProperties.write(keydict, '/tmp')

if __name__ == "__main__":
    main(sys.argv[1:])
