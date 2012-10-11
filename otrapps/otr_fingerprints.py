#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    def write(keys, filename):
        tsv = csv.writer(open(filename, 'w'), delimiter='\t')
        for key in keys:
            if 'fingerprint' in key:
                # TODO look up accounts to associate remote accounts to
                row = ['PLACEHOLDER', key['name'], key['protocol'], key['fingerprint']]
                if 'verification' in key and key['verification'] != None:
                    row.append(key['verification'])
                tsv.writerow(row)


if __name__ == '__main__':

    import sys
    import pprint
    pprint.pprint(OtrFingerprints.parse(sys.argv[1]))
