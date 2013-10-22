#!/bin/sh
#
# this is the script run by the Jenkins server to run the build and tests.  Be
# sure to always run it in its dir, i.e. ./run-tests.sh, otherwise it might
# remove things that you don't want it to.

if [ `dirname $0` != "." ]; then
    echo "only run this script like ./`basename $0`"
    exit
fi

set -e
set -x

if [ -z $WORKSPACE ]; then
    WORKSPACE=`pwd`
fi

# run tests
cd $WORKSPACE/tests
./run-tests.sh

#------------------------------------------------------------------------------#
# test install using site packages
rm -rf $WORKSPACE/env
virtualenv --system-site-packages $WORKSPACE/env
. $WORKSPACE/env/bin/activate
pip install -e $WORKSPACE

# run tests in new pip+virtualenv install
. $WORKSPACE/env/bin/activate
keysync=$WORKSPACE/env/bin/keysync $WORKSPACE/tests/run-tests.sh

#------------------------------------------------------------------------------#
# test install using packages from pypi
rm -rf $WORKSPACE/env
virtualenv --no-site-packages $WORKSPACE/env
. $WORKSPACE/env/bin/activate
pip install -e $WORKSPACE

# run tests in new pip+virtualenv install
. $WORKSPACE/env/bin/activate
keysync=$WORKSPACE/env/bin/keysync $WORKSPACE/tests/run-tests.sh
