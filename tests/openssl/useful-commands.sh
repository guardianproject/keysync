#!/bin/sh
#
# this script uses openssl to generate a standard OTR DSA key or 3072 bits

# generate a new unencrypted DSA key
openssl dsaparam -out dsaparam.pem 3072
openssl gendsa -out private-key-openssl.pem dsaparam.pem

# convert public key to PKCS#1/X.509 format
openssl dsa -in private-key-openssl.pem -pubout -out public-key-PKCS\#1-X.509.pem

# convert private key to a PKCS#8 format
openssl pkcs8 -nocrypt -in private-key-openssl.pem -topk8 -out private-key-PKCS\#8.pem

# convert PKCS#8 private key to a java properties file
propfile=private-key-PKCS\#8.properties
printf "privateKey=" > $propfile
echo `cat private-key-PKCS#8.pem | grep -v -- '-----'` | sed 's, ,,g' | sed 's,=,\\=,g' >> $propfile

# convert PKCS #1/X.509 public key to a java properties file
printf "publicKey=" >> $propfile
echo `cat public-key-pkcs1-X.509.pem | grep -v -- '-----'` | sed 's, ,,g' | sed 's,=,\\=,g' >> $propfile
