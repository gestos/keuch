#!/usr/bin/python
import sys
import os

print sys.argv[1]           # this is the first command line argument
toplevel = sys.argv[1]      # from now on called toplevel
print (toplevel)            # as we see, it's the same

for aa, bb, cc in os.walk(toplevel):  # the python for does not need a termination like do<->done in bash
    if not bb:                                    # no dirnames=leaf node
        print aa
