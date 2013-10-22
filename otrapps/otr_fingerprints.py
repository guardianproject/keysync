#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''a module for reading and writing libotr's public key data'''

from __future__ import print_function
import csv

class OtrFingerprints():

    @staticmethod
    def parse(filename):
        '''parse the otr.fingerprints file and return a list of keydicts'''
        tsv = csv.reader(open(filename, 'r'), delimiter='\t')
        keydict = dict()
        for row in tsv:
            key = dict()
            name = row[0].strip()
            key['name'] = name
            key['protocol'] = row[2].strip()
            key['fingerprint'] = row[3].strip()
            key['verification'] = row[4].strip()
            keydict[name] = key
        return keydict

    @staticmethod
    def _includexmppresource(accounts, resources):
        '''pidgin requires the XMPP Resource in the name of the associated account'''
        returnlist = []
        for account in accounts:
            if account in resources.keys():
                returnlist.append(account + '/' + resources[account])
            else:
                returnlist.append(account + '/' + 'ReplaceMeWithActualXMPPResource')
        return returnlist

    @staticmethod
    def write(keydict, filename, accounts, resources=None):
        if resources:
            accounts = OtrFingerprints._includexmppresource(accounts, resources)
        # we have to use this list 'accounts' rather than the private
        # keys in the keydict in order to support apps like Adium that
        # don't use the actual account ID as the index in the files.
        tsv = csv.writer(open(filename, 'w'), delimiter='\t')
        for name, key in keydict.items():
            if 'fingerprint' in key:
                for account in accounts:
                    row = [name, account, key['protocol'], key['fingerprint']]
                    if 'verification' in key and key['verification'] != None:
                        row.append(key['verification'])
                    tsv.writerow(row)


if __name__ == '__main__':

    import sys
    import pprint
    keydict = OtrFingerprints.parse(sys.argv[1])
    pprint.pprint(keydict)
    accounts = [ 'gptest@jabber.org', 'gptest@limun.org', 'hans@eds.org']
    OtrFingerprints.write(keydict, 'otr.fingerprints', accounts)
