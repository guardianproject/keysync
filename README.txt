
This project is for converting the various OTR file formats between
each other.  We are focusing on two major versions: libotr format and
otr4j, and then a few variants of those major formats.

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

otr4j
-----

Gibberbot:
  /data/data/info.guardianproject.otr.im.app/files/otr_keystore

  All OTR information is stored in a single Java .properties
  file. Private keys, public key fingerprints, and verification status
  are each individual properties.

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
