#!/usr/bin/python

import sys
import re

if len(sys.argv) < 2:
    sys.stderr.write("Usage: {} <profile_binary>\n".format(sys.argv[0]))
    sys.exit(1)

profile = sys.argv[1]

skip_operations = [
    "accept", "bind", "connect", "getsockname", "getsockopt",
    "recvmsg", "sendmsg", "setsockopt", "socket_shutdown",
]

for line in sys.stdin.readlines():
    if not profile in line:
        continue

    match_operation = re.match('^.* operation="(.*?)" .*', line)
    if match_operation is not None:
        operation = match_operation.groups()[0]
        if operation not in skip_operations:
            match_name = re.match('^.* name="(.*?)" .*', line)
            if match_name:
                name = match_name.groups()[0]
                print name

