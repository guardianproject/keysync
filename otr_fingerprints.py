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
            if row[1].find('/') > -1:
                name, resource = row[1].split('/')
                keydict['name'] = name
                keydict['resource'] = resource
            else:
                keydict['name'] = row[1]
                keydict['resource'] = ''
            keydict['protocol'] = row[2]
            keydict['fingerprint'] = row[3]
            keydict['verification'] = row[4]
            keys.append(keydict)
        return keys

if __name__ == '__main__':

    import sys
    import pprint
    pprint.pprint(OtrFingerprints.parse(sys.argv[1]))
