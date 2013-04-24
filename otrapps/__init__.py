import os
__all__ = ['adium', 'gibberbot', 'irssi', 'jitsi', 'pidgin', 'gajim',]

apps_supported = __all__
apps_supported.append('all')

def make_outdir(output_folder, subdir):
    dir = os.path.join(output_folder, subdir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


