#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

class OtrFingerprints():

    @staticmethod
    def parse(filename):
        '''parse the otr.fingerprints file and return a list of keydicts'''
        tsv = csv.reader(open(filename, 'r'), delimiter='\t')
        keys = []
        for row in tsv:
            keydict = {}
            keydict['name'] = row[0].strip()
            keydict['protocol'] = row[2].strip()
            keydict['fingerprint'] = row[3].strip()
            keydict['verification'] = row[4].strip()
            keys.append(keydict)
        return keys

    @staticmethod
    def write(keys, filename):
        tsv = csv.writer(open(filename, 'w'), delimiter='\t')
        for key in keys:
            if 'fingerprint' in key:
                print 'ROW ROW ROW'
                print key
                # TODO look up accounts to associate remote accounts to
                row = ['PLACEHOLDER', key['name'], key['protocol'], key['fingerprint']]
                if 'verification' in key and key['verification'] != None:
                    row.append(key['verification'])
                tsv.writerow(row)


if __name__ == '__main__':

    import sys
    import pprint
    pprint.pprint(OtrFingerprints.parse(sys.argv[1]))
