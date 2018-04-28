#!/bin/sh

#
# When people import a full mysql dump, the debian-sys-maint user stops
# working, which causes problems with logrotation.
#
# This script automatically fixes that problem by resetting the
# debian-sys-maint password back to the value mentioned in the configuration
# file.
#
# NOTE: This assumes we're allowed to connect to mysql without a password as
# the root user.

DEBIANCNF="/etc/mysql/debian.cnf"
BIN_MYSQL="/usr/bin/mysql"

if [ -f "$DEBIANCNF" ]; then
    # Config file exists. Read password.
    PASSWORD=$(grep "^password" /etc/mysql/debian.cnf | head -n1 | sed 's/^password\s*=\s*\(.*\)\s*$/\1/')
    if [ -z "$PASSWORD" ]; then
        echo "Missing password?" >&2
        exit 1
    fi
	# FIXME
fi
