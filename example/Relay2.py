import os, sys
# Import needed python files from parent path of the example folder
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Relay import Relay

if __name__ == '__main__':
    relay2 = Relay(parentPath + '/config/host_R3.ini')
