#!/bin/sh

set -e

cd ../otrapps

for app in adium chatsecure gajim gpg irssi jitsi pidgin xchat util; do
    echo ''
    echo ''
    echo '------------------------------------------------------------------------'
    echo $app
    echo '------------------------------------------------------------------------'
    python ./$app.py
done

