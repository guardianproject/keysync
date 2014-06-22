
'''sets up the otrapps module with all of the currently supported apps'''

import os
import sys

from pkg_resources import get_distribution, DistributionNotFound
try:
    _dist = get_distribution('keysync')
    if not __file__.startswith(os.path.join(_dist.location, 'otrapps')):
        raise DistributionNotFound
except DistributionNotFound:
    # probably running from source repo or another version is installed
    __version__ = '(local version)'
else:
    __version__ = _dist.version


__all__ = ['adium', 'chatsecure', 'irssi', 'jitsi', 'pidgin', 'gajim', 'gnupg', 'xchat', 'kopete',]

if __name__ == '__main__':
    sys.path.insert(0, "../") # so the main() test suite can find otrapps module
import otrapps.adium
import otrapps.chatsecure
import otrapps.irssi
import otrapps.jitsi
import otrapps.pidgin
import otrapps.gajim
import otrapps.gnupg
import otrapps.xchat
import otrapps.kopete

apps = { 'adium'     : otrapps.adium.AdiumProperties,
         'chatsecure': otrapps.chatsecure.ChatSecureProperties,
         'irssi'     : otrapps.irssi.IrssiProperties,
         'jitsi'     : otrapps.jitsi.JitsiProperties,
         'pidgin'    : otrapps.pidgin.PidginProperties,
         'gajim'     : otrapps.gajim.GajimProperties,
         'gnupg'     : otrapps.gnupg.GnuPGProperties,
         'xchat'     : otrapps.xchat.XchatProperties,
         'kopete'    : otrapps.kopete.KopeteProperties,
        }
apps_supported = apps.keys()

def make_outdir(output_folder, subdir):
    '''create the folder that the results will be written to'''
    outdir = os.path.join(output_folder, subdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    return outdir


