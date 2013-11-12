#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''a module for reading and writing ChatSecure's OTR key data'''

from __future__ import print_function
import hashlib
import os
import sys
import pyjavaproperties
import subprocess
import tempfile

if __name__ == '__main__':
    sys.path.insert(0, "../") # so the main() test suite can find otrapps module
import otrapps.util

class ChatSecureProperties():

    path = '/data/data/info.guardianproject.otr.app.im/files/otr_keystore'
    keyfile = 'otr_keystore'
    encryptedkeyfile = keyfile + '.ofcaes'
    files = (keyfile, encryptedkeyfile)

    password = None

    @staticmethod
    def parse(filename):
        '''parse the given file into the standard keydict'''
        # the parsing and generation is done in separate passes so that
        # multiple properties are combined into a single keydict per account,
        # containing all of the fields
        p = pyjavaproperties.Properties()
        p.load(open(filename))
        parsed = []
        for item in p.items():
            propkey = item[0]
            if propkey.endswith('.publicKey'):
                id = '.'.join(propkey.split('.')[0:-1])
                parsed.append(('public-key', id, item[1]))
            elif propkey.endswith('.publicKey.verified'):
                keylist = propkey.split('.')
                fingerprint = keylist[-3]
                id = '.'.join(keylist[0:-3])
                parsed.append(('verified', id, fingerprint))
            elif propkey.endswith('.privateKey'):
                id = '.'.join(propkey.split('.')[0:-1])
                parsed.append(('private-key', id, item[1]))
        # create blank keys for all IDs
        keydict = dict()
        for keydata in parsed:
            name = keydata[1]
            if not name in keydict:
                keydict[name] = dict()
                keydict[name]['name'] = name
                keydict[name]['protocol'] = 'prpl-jabber'
            if keydata[0] == 'private-key':
                cleaned = keydata[2].replace('\\n', '')
                numdict = otrapps.util.ParsePkcs8(cleaned)
                for num in ('g', 'p', 'q', 'x'):
                    keydict[name][num] = numdict[num]
            elif keydata[0] == 'verified':
                keydict[name]['verification'] = 'verified'
                fingerprint = keydata[2].lower()
                otrapps.util.check_and_set(keydict[name], 'fingerprint', fingerprint)
            elif keydata[0] == 'public-key':
                cleaned = keydata[2].replace('\\n', '')
                numdict = otrapps.util.ParseX509(cleaned)
                for num in ('y', 'g', 'p', 'q'):
                    keydict[name][num] = numdict[num]
                fingerprint = otrapps.util.fingerprint((numdict['y'], numdict['g'], numdict['p'], numdict['q']))
                otrapps.util.check_and_set(keydict[name], 'fingerprint', fingerprint)
        return keydict

    @staticmethod
    def write(keydict, savedir, password=None):
        '''given a keydict, generate a chatsecure file in the savedir'''
        p = pyjavaproperties.Properties()
        for name, key in keydict.items():
            # only include XMPP keys, since ChatSecure only supports XMPP
            # accounts, so we avoid spreading private keys around
            if key['protocol'] == 'prpl-jabber' or key['protocol'] == 'prpl-bonjour':
                if 'y' in key:
                    p.setProperty(key['name'] + '.publicKey', otrapps.util.ExportDsaX509(key))
                if 'x' in key:
                    if not password:
                        h = hashlib.sha256()
                        h.update(os.urandom(16)) # salt
                        h.update(bytes(key['x']))
                        password = h.digest().encode('base64')
                    p.setProperty(key['name'] + '.privateKey', otrapps.util.ExportDsaPkcs8(key))
            if 'fingerprint' in key:
                p.setProperty(key['name'] + '.fingerprint', key['fingerprint'])
            if 'verification' in key and key['verification'] != None:
                p.setProperty(key['name'] + '.' + key['fingerprint'].lower()
                              + '.publicKey.verified', 'true')
        fd, filename = tempfile.mkstemp()
        f = os.fdopen(fd, 'w')
        p.store(f)

        # if there is no password, then one has not been set, or there
        # are not private keys included in the file, so its a lower
        # risk file. Encryption only needs to protect the meta data,
        # not the private keys.  Therefore, its not as bad to generate
        # a "random" password here
        if not password:
            password = os.urandom(32).encode('base64')

        # create passphrase file from the first private key
        cmd = ['openssl', 'aes-256-cbc', '-pass', 'stdin', '-in', filename,
               '-out', os.path.join(savedir, 'otr_keystore.ofcaes')]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ChatSecureProperties.password = password
        print((p.communicate(password)))

    @staticmethod
    def _decrypt_ofcaes(ofcaes_filename, password):
        ''' Decrypt an encrypted key file (with user-supplied password).'''
        # It might be a bad idea to write out this unencrypted file.

        # get a tmp place to put the decrypted file
        fd, filename = tempfile.mkstemp()
        f = os.fdopen(fd, 'w')
        f.close()

        # same as above, but with the -d flag to decrypt
        cmd = ['openssl', 'aes-256-cbc', '-d', '-pass', 'stdin', '-in', ofcaes_filename,
       '-out', filename]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.communicate(password)
        return filename


#------------------------------------------------------------------------------#
# for testing from the command line:
def main(argv):
    import pprint

    print('ChatSecure stores its files in ' + ChatSecureProperties.path)

    if len(sys.argv) == 2:
        settingsfile = sys.argv[1]
    else:
        settingsfile = '../tests/chatsecure/otr_keystore'

    p = ChatSecureProperties.parse(settingsfile)
    print('----------------------------------------')
    pprint.pprint(p)
    print('----------------------------------------')

if __name__ == "__main__":
    main(sys.argv[1:])
