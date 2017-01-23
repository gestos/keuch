#!/usr/bin/python

import sys
import os
import hashlib

folder = sys.argv[1]
## 53 und 69 sind das selbe datum
for a in os.listdir(folder):
    full=os.path.join(folder, a)
    print (str(full) + " " + str(os.stat(full).st_size))
    print (hashlib.sha256(full).hexdigest())
