#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
import pprint


if __name__ == '__main__':

    tsv = csv.reader(open(sys.argv[1], 'r'), delimiter='\t')
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
    pprint.pprint(keys)

