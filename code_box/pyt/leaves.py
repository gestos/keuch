#!/usr/bin/python
import sys
import os

print sys.argv[1]
toplevel = sys.argv[1]
print (toplevel)

for dirpath, dirnames, filenames in os.walk(toplevel):
    if not dirnames:
        print dirpath
