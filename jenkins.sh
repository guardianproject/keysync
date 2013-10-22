#!/bin/sh
#
# this is the script run by the Jenkins server to run the build and tests

set -e
set -x

if [ -z $WORKSPACE ]; then
    WORKSPACE=`pwd`
fi

# run tests
cd $WORKSPACE/tests
./run-tests.sh

# test install
rm -rf $WORKSPACE/env
virtualenv --system-site-packages $WORKSPACE/env
. $WORKSPACE/env/bin/activate
pip install -e $WORKSPACE

# test new install
$WORKSPACE/env/bin/keysync
