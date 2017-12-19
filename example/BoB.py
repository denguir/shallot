import os, sys
# Import needed python files from parent path of the example folder
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Receiver import Receiver

if __name__ == '__main__':
    Bob = Receiver(parentPath + '/config/host_R4.ini')
