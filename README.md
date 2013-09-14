
KeySync - One key for all of your chat apps
===========================================

There are many chat apps that support OTR encryption for verifying messages.
Many of us use multiple chat apps, including one for desktop and another for
mobile, or one for Mac OS X and another for GNU/Linux or Windows.  The trust
relationships are only stored locally in the app in a format that is specific
to that app.  Switching between all of them means that you have to manage your
trust relationships for each app that you use.

KeySync addresses this problem by allowing you to sync your OTR identity and
trust relationships between multiple apps.  It currently works with ChatSecure
on Android, and Pidgin, Adium, and Jitsi on desktop.

How to sync
-----------

To sync between ChatSecure and your desktop apps, plug in your phone or device
via USB and run the sync.  Or you can manually copy the `otr_keystore.ofcaes`
file over to your device's SD Card, where ChatSecure looks for it.  Using
ChatSecure, you will need to scan the QRCode that KeySync shows you in order
to complete the sync.  The `otr_keystore.ofcaes` file is encrypted to prevent
your private information from leaking out.  That QRCode is the password to
your keystore, so do not share it with anyone.

If you have multiple chat apps that you use, or you are switching from one to
another, you can use KeySync to sync up the trust relationships between
multiple desktop apps.  Here's how:

1. quit all of the chat apps that you want to
2. select whichever apps you want to sync
3. then run the sync

Now, open your chat apps and you should have synced trust!  In case of
problems, it saved your original OTR files in place.  They are named using a
long string of numbers that represent the time when they were backed up.

This is beta software, do not rely on it for strong identity verification.  It
is unlikely to mess up so bad as to produce compromised private keys, but
anything is possible.  Also, keep in mind that program is handling your
private OTR keys, so make sure that you don't copy, send or email the
`otr_keystore.ofcaes` file somewhere unsafe.  All that said, testing
and feedback is greatly appreciated, so we can get it to the point where we
can trust it.


Adding apps to KeySync
----------------------

This project has libraries for converting the various OTR file formats between
each other.  We have focused on the two major versions: libotr format and otr4j,
and then a few variants of those major formats.  All OTR implementations can
be supported as long as they can be read and parsed by Python.

KeySync has preliminary support for Gajim and IRSSI, and it has a modular
architecture to allow for expansion.  If you want to add an app that is not
already included, you just need to make a single python file that converts
between that app's OTR data format and the KeySync internal format (documented
below).


Reporting bugs
--------------

We appreciate all feedback, be it bug reports, patches, pull requests, feature
requests, etc.  Please add your bugs and requests to our issue tracker:

https://dev.guardianproject.info/projects/keysync/issues

Email us at support@guardianproject.info with questions, problems, etc., or
just to let us know that you are using KeySync and find it useful.


INSTALL
=======

List of python dependencies:

* pycrypto - https://www.dlitz.net/software/pycrypto/
* pyparsing - http://pyparsing.wikispaces.com
* pyjavaproperties - http://pypi.python.org/pypi/pyjavaproperties
* python-pgpdump - https://pypi.python.org/pypi/pgpdump/
* argparse - native in >= 2.7, else https://code.google.com/p/argparse/
* pure-python-otr - https://github.com/afflux/pure-python-otr
* gnupg-interface - http://py-gnupg.sourceforge.net/
* pyasn - https://code.google.com/p/pyasn/
* beautifulsoup 3 - http://www.crummy.com/software/BeautifulSoup/
* qrcode - https://github.com/lincolnloop/python-qrcode


Debian/Ubuntu/Mint/etc
----------------------

We're working to get all packages into official Debian/Ubuntu/etc. releases,
in the meantime you can install KeySync by adding our PPA (fingerprint
F50EADDD2234F563):

    sudo add-apt-repository ppa:guardianproject/ppa
    sudo apt-get update
    sudo apt-get install keysync

PPA URL: https://launchpad.net/~guardianproject/+archive/ppa

If you want to install the dependencies because you're going to develop
KeySync, then install them manually with:

    sudo apt-get install python-pyparsing python-pyasn1 python-potr \
      python-pyjavaproperties python-beautifulsoup python-qrcode \
      python-pgpdump python-crypto

For Debian, you can try using the Ubuntu PPA, with something like oneiric for
wheezy, and natty for squeeze:

  deb http://ppa.launchpad.net/guardianproject/ppa/ubuntu oneiric main


Mac OS X
--------

For Mac OS X, you can download the binary app from our website:
https://guardianproject.info


You can also install KeySync using Fink:

    fink install pycrypto-py27 pyparsing-py27 pyjavaproperties-py27 argparse-py27 \
        python-potr-py27 gnupg-interface-py27 pyasn1-py27 beautifulsoup-py27


Windows
-------

For Windows, you can download the binary app from our website:
https://guardianproject.info


Fedora/Redhat/RPMs
------------------

Install these build dependencies locally, then follow the instructions for
pip+virtualenv below:

    sudo yum install gmp-devel tk


pip+virtualenv install
------------------

Activate your virtual python environment then:
        pip install -Ur python-deps.txt


=====
USAGE
=====

Currently, the code allows for reading multiple file formats into a python
dictionary form.  The only export method currently activated is for Gibberbot
format in a file called otr_keystore.ofcaes.  To use, point the `keysync`
script the app that you want to read OTR info from, and it will generate
`otr_keystore` to send to Gibberbot on your Android device (run
`keysync --help` to see all currently available options).

  keysync --input pidgin


=======
FORMATS
=======

libotr
------

Adium:
  ~/Library/Application Support/Adium 2.0/Users/Default/otr.private_key
  ~/Library/Application Support/Adium 2.0/Users/Default/otr.fingerprints
  ~/Library/Application Support/Adium 2.0/Users/Default/Accounts.plist

  Uses the standard libotr files and overall file format for
  otr.private_key and otr.fingerprints.  Account ID is stored as an
  integer which must be referenced from the Accounts.plist to get the
  actuall XMPP account name (e.g. me@jabber.org). Uses full word
  descriptive tags for the various protocols, e.g. libpurple-oscar-AIM,
  libpurple-Jabber, etc.

Pidgin
 GNU/Linux
  ~/.purple/otr.private_key
  ~/.purple/otr.fingerprints
 Windows
  ~/Application Data/.purple/otr.private_key
  ~/Application Data/.purple/otr.fingerprints

  Uses the standard libotr files and overall file format for
  otr.private_key and otr.fingerprints. Account IDs are used directly
  in the libotr files. XMPP/Jabber Account IDs include the "Resource"
  e.g. me@jabber.org/Resource or me@jabber.org/Pidgin.

irssi
  ~/.irssi/otr/otr.key
  ~/.irssi/otr/otr.fp

  Uses the standard libotr file format and files, but names the files
  differently, basically abbreviated versions of the libotr names.
  Account IDs are used directly in the libotr files.

xchat
  ~/.xchat2/otr/otr.key
  ~/.xchat2/otr/otr.fp

  Same as irssi

otr4j
-----

Gibberbot:
  /data/data/info.guardianproject.otr.app.im/files/otr_keystore

  All OTR information is stored in a single Java .properties
  file. Private keys, public key fingerprints, and verification status
  are each individual properties.  This format also includes the
  storage of the remote public keys, unlike libotr.  otr4j
  implementations load the remote public key from the store rather
  than always getting it from the OTR session.

Jitsi:
 GNU/Linux
  ~/.jitsi/sip-communicator.properties
  ~/.jitsi/contactlist.xml
 Mac OS X
  ~/Library/Application Support/Jitsi/sip-communicator.properties
  ~/Library/Application Support/Jitsi/contactlist.xml
 Windows
  ~/Application Data/Jitsi/sip-communicator.properties
  ~/Application Data/Jitsi/contactlist.xml

  All app settings are stored in a single Java .properties file,
  including OTR information. Private keys, public key fingerprints,
  and verification status are each individual properties.


pure-python-otr
---------------

pure-python-otr is pure python implementation of the OTR spec.  It
includes newer features like Socialist Millionaire's Protocol.  The
private key is stored in a separate file per-account.  The
fingerprints are stored in the same tab-separated-value format as
libotr but with a fingerprint file per-account.

Gajim:
  GNU/Linux:
    ~/.local/share/gajim/_SERVERNAME_.key3
    ~/.local/share/gajim/_SERVERNAME_.fpr
    ~/.config/gajim/config
  Windows:
    ~/Application Data/Gajim/


keyczar
-------

KeyCzar stores keys in JSON files with two different formats: 0.5b and
0.6b.  It uses a special base64 encoding with a URL-safe alphabet:
  - replaces +
  _ replaces /

http://code.google.com/p/keyczar/wiki/DsaPrivateKey
http://code.google.com/p/keyczar/wiki/DsaPublicKey

 0.6b
  public:
    "q": The DSA subprime
    "p": The DSA prime
    "g": The DSA base
    "y": The DSA public key exponent
    "size" : The size of the modulus in bits
  private:
    "publicKey": The JSON representation of the corresponding DsaPublicKey
    "x": The secret exponent of this private key
    "size" : The size of the modulus in bits

 0.5b
  public:
     "x509": A WebSafeBase64 encoded X509 representation
  private:
     "pkcs8": A WebSafeBase64 encoded PKCS#8 representation of the private key
     "publicKey": A WebSafeBase64 encoding of the key's corresponding DsaPublicKey


ZRTP
----

A ZID record stores (caches) ZID (ZRTP ID) specific data that helps
ZRTP to achives its key continuity feature. Please refer to the ZRTP
specification to get detailed information about the ZID.

 ZRTP key types:
  2048 bit Diffie-Helman values
  3072 bit Diffie-Helman values
  256 bit Diffie-Helman elliptic curve
  384 bit Diffie-Helman elliptic curve



IMPLEMENTATION
==============

The key idea in the implementation is to get everything into a common format
internally.  That common format can then be handed to any class for a given
program, which knows how to output it to the correct file format.  The current
internal data format is a dict of dicts representing a key, called 'keydict'.
So first, you have a dict representing a given account with a given key
associated with it.  This account name is used as the unique ID.  Then the
whole collection of keys, both local private keys and remote public keys, are
collected in meta dict with the account name as the key and the whole dict as
the value. This format allows for easy merging, which enables syncing between
files.

Sample structure in python dict notation:

    keydict = {
        'userid': {
                    'fingerprint': 'ff66e8c909c4deb51cbd4a02b9e6af4d6af215f8',
                    'name': 'userid',
                    'protocol': 'IRC',
                    'resource': 'laptop', # the XMPP "resource"
                    'verification': 'verified', # or 'smp' for Socialist Millionares
                    'p': '<p value>', # public part of the DSA key
                    'q': '<q value>', # public part of the DSA key
                    'g': '<g value>', # public part of the DSA key
                    'x': '<x value>', # core of private DSA key
                    'y': '<y value>', # core of public DSA key
                },
        'userid2' : { ... },
        ...
        'useridn' : { ... }
    }

