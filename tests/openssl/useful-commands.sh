#!/bin/sh
#
# this script uses openssl to generate a standard OTR DSA key or 3072 bits

openssl_key=private-key-openssl.pem
x509_key=public-key-PKCS\#1-X.509.pem
pkcs8_key=private-key-PKCS\#8.pem
propfile=dsa-key.properties

# generate a new unencrypted DSA key
openssl dsaparam -out dsaparam.pem 3072
openssl gendsa -out $openssl_key dsaparam.pem

# convert public key to PKCS#1/X.509 format
openssl dsa -in $openssl_key -pubout -out $x509_key

# convert private key to a PKCS#8 format
openssl pkcs8 -nocrypt -in $openssl_key -topk8 -out $pkcs8_key

# convert PKCS#8 private key to a java properties file
printf "privateKey=" > $propfile
echo `cat $pkcs8_key | grep -v -- '-----'` | sed 's, ,,g' | sed 's,=,\\=,g' >> $propfile

# convert PKCS #1/X.509 public key to a java properties file
printf "publicKey=" >> $propfile
echo `cat $x509_key | grep -v -- '-----'` | sed 's, ,,g' | sed 's,=,\\=,g' >> $propfile
