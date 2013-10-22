#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import pgpdump


class GnuPGProperties():

    path = os.path.expanduser('~/.gnupg')
    secring = 'secring.gpg'
    pubring = 'pubring.gpg'
    files = (secring, pubring)

    @staticmethod
    def parse(settingsdir=None):
        if settingsdir == None:
            settingsdir = GnuPGProperties.path

        secring_file = os.path.join(settingsdir, GnuPGProperties.secring)
        if not os.path.exists(secring_file):
            return dict()
        rawdata = GnuPGProperties.load_data(secring_file)
        try:
            data = pgpdump.BinaryData(rawdata)
        except pgpdump.utils.PgpdumpException, e:
            print("gnupg: %s" % (e))
            return dict()
        packets = list(data.packets())

        names = []
        keydict = dict()
        for packet in packets:
            values = dict()
            if isinstance(packet, pgpdump.packet.SecretSubkeyPacket):
                if packet.pub_algorithm_type == "dsa":
                    values['p'] = packet.prime
                    values['q'] = packet.group_order
                    values['g'] = packet.group_gen
                    values['y'] = packet.key_value
                    values['x'] = packet.exponent_x
                    # the data comes directly from secret key, mark verified
                    values['verification'] = 'verified'
                    values['fingerprint'] = packet.fingerprint
            elif isinstance(packet, pgpdump.packet.UserIDPacket):
                names.append(str(packet.user_email)) # everything is str, not unicode
            if 'fingerprint' in values.keys():
                for name in names:
                    keydict[name] = values
                    keydict[name]['name'] = name
                    keydict[name]['protocol'] = 'prpl-jabber' # assume XMPP for now
        return keydict

    @staticmethod
    def write(keys, savedir):
        print('Writing GnuPG output files is not yet supported!')

    @staticmethod
    def load_data(filename):
        with open(filename, 'rb') as fileobj:
            data = fileobj.read()
        return data


if __name__ == '__main__':

    import pprint

    print('GnuPG stores its files in ' + GnuPGProperties.path)

    if len(sys.argv) == 2:
        settingsdir = sys.argv[1]
    else:
        settingsdir = '../tests/gnupg'

    l = GnuPGProperties.parse(settingsdir)
    pprint.pprint(l)
