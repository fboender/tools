#!/usr/bin/env python

import sys
import time
import re

if not len(sys.argv) > 1:
    print "Usage: %s FILE" % (sys.argv[0])
    sys.exit(1)

mtypesColors = {}
mtypesColors["php fatal error"] = "[%s] \x1b[0;37;41mFatal   Error\x1b[0m in %s(%s): \x1b[1;37;40m%s\x1b[0m"
mtypesColors["php parse error"] = "[%s] \x1b[1;31;40mParse   Error\x1b[0m in %s(%s): \x1b[1;37;40m%s\x1b[0m"
mtypesColors["php warning"]     = "[%s] \x1b[1;33;40mWarn    Error\x1b[0m in %s(%s): \x1b[1;37;40m%s\x1b[0m"
mtypesColors["php notice"]      = "[%s] \x1b[1;36;40mNotice  Error\x1b[0m in %s(%s): \x1b[1;37;40m%s\x1b[0m"
mtypesColors["php user error"]  = "[%s] \x1b[1;34;40mUser    Error\x1b[0m in %s(%s): \x1b[1;37;40m%s\x1b[0m"
mtypesColors["runtime notice"]  = "[%s] \x1b[1;35;40mRuntime Error\x1b[0m in %s(%s): \x1b[1;37;40m%s\x1b[0m"
mtypesColors["unknown"]         = "\x1b[2;37;41m%s\x1b[0m"

re = re.compile("^\[(.*?)\] (.*?): (.*?) in /(.*) on line (.*)");

try:
    f = file(sys.argv[1])
    f.seek(0, 2) # Move to EOF
    new = False
    while 1:
        lines = f.readlines()
        if lines:
            for line in lines:
                new = True
                line = line.strip()
                match = re.match(line)

                if match:
                    mdate, mtype, merror, mfile, mline = match.groups()
                    mdate = mdate[11:19]
                    if mfile.find("htdocs/"):
                        mfile = mfile[mfile.find("htdocs/")+7:]

                    try:
                        print mtypesColors[mtype.lower()] % (mdate, mfile, mline, merror)
                    except KeyError, e:
                        print mtypesColors["unknown"] % (line)
                else:
                    print mtypesColors["unknown"] % (line)

        if new:
            print ""
            new = False

        time.sleep(0.5)
except KeyboardInterrupt, e:
    f.close()
    sys.exit(0)

