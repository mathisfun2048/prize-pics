import sys # imports python's system module allows us to access paths
import os # imports os module, allows us to move files accross paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

'''
this line does quite a bit:
__file__ is the location of this script
.. means go up one directory
lib means access lib folder
insert(0, ...) means that this is the first place python looks for imports

These together makes importing the waveshare library easier
'''

from waveshare_epd import epd4in2_V2 # this is tfdshe library!

