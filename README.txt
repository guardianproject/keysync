
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
  ~/.purple/otr.private_key
  ~/.purple/otr.fingerprints

  Uses the standard libotr files and overall file format for
  otr.private_key and otr.fingerprints. Account IDs are used directly
  in the libotr files. XMPP/Jabber Account IDs include the "Resource"
  e.g. me@jabber.org/Resource or me@jabber.org/Pidgin.

otr4j
-----

Gibberbot:
  /data/data/info.guardianproject.otr.im.app/files/otr_keystore

  All OTR information is stored in a single Java .properties
  file. Private keys, public key fingerprints, and verification status
  are each individual properties.

Jitsi:
  ~/.jitsi/sip-communicator.properties
  ~/Library/Application Support/Jitsi/sip-communicator.properties

  All app settings are stored in a single Java .properties file,
  including OTR information. Private keys, public key fingerprints,
  and verification status are each individual properties.
