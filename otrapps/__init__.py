
__all__ = ['adium', 'gibberbot', 'irssi', 'jitsi', 'pidgin', ]

def make_outdir(output_folder, subdir):
    dir = os.path.join(output_folder, subdir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


