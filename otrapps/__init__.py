import os
__all__ = ['adium', 'chatsecure', 'irssi', 'jitsi', 'pidgin', 'gajim', 'gpg', 'xchat',]

import adium, chatsecure, irssi, jitsi, pidgin, gajim, gpg, xchat
apps = { 'adium'     : adium.AdiumProperties,
         'chatsecure' : chatsecure.ChatSecureProperties,
         'irssi'     : irssi.IrssiProperties,
         'jitsi'     : jitsi.JitsiProperties,
         'pidgin'    : pidgin.PidginProperties,
         'gajim'     : gajim.GajimProperties,
         'gpg'       : gpg.GPGProperties,
         'xchat'     : xchat.XchatProperties,
        }
apps_supported = apps.keys()

def make_outdir(output_folder, subdir):
    dir = os.path.join(output_folder, subdir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


