"""
piswitch is control code for a raspberry pi GPIO-based lightswitch.
"""
from distutils.core import setup
import glob

if __name__ == '__main__':
    setup(name = 'piswitch',
        description = __doc__,
        long_description = __doc__,
        license = 'GPL',
        author = 'Rachel Simone Domagalski',
        author_email = 'rsdomagalski@gmail.com',
        url = 'https://github.com/domagalski/piswitch',
        py_modules = ['piswitch'],
        scripts = glob.glob('powerswitch_?x.py'),
    )
