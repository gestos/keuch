#!/usr/bin/python
import sys
import os
import magic    # this is for filetpyes
from eyed3 import id3

print sys.argv[1]           # this is the first command line argument
toplevel = sys.argv[1]      # from now on called toplevel
print (toplevel)            # as we see, it's the same

for pathname,subdirs,files in os.walk(toplevel, topdown=False):  # the python for does not need a termination like do<->done in bash
    if not subdirs:                                    # no dirnames=leaf node
        print pathname
        print type(files)
        for eachfile in files:
            print "\n"
            print eachfile
            fullfile = os.path.join(pathname,eachfile)
            print type(fullfile)
            # print magic.from_file(fullfile)

            tag = id3.Tag()
            print type(tag)
            tag.parse(fullfile)
            print tag.parse(fullfile)
            # print(tag.artist)
            print(tag.isV1)
            print tag.isV2("/media/mucke-local/alan watts - still the mind - introduction to meditation/Alan Watts - Still the Mind - Introduction to Meditation-002.mp3")
            print(tag.isV2)
#            print help(id3.Tag)

