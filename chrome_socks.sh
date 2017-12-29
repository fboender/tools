#!/bin/bash

# Start a Chrome(ium) browser on a Socks 5 proxy. This causes all traffic in
# the browser to travel through the proxy, which makes it seem like the browser
# is running remotely. This is useful for access resources on private networks
# without having to set up a manual tunnel or traditional VPN.

BROWSERS="chromium-browser google-chrome"

HOST=$1; shift;
SITES=$*

if [ -z "$HOST" ]; then
    echo "Usage; $0 <HOST>"
    exit 1
fi

# Find Google Chrom(e|ium)
echo "Determining browser binary"
for BROWSER_NAME in $BROWSERS; do
	BROWSER_BIN=$(which $BROWSER_NAME)
done
if [ -z "$BROWSER_BIN" ]; then
	echo "No Chrome-like browser found (looked for $BROWSERS). You may want to edit $0 and add it manually"
	exit 1
fi
echo "Using browser: $BROWSER_BIN"

# Find random port, start ssh socks proxy and browser
while `true`;
do
	echo "Finding random unused port"
    PORT=$(expr 8000 + $RANDOM / 32) # random port in range 8000 - 9000
    if [ \! "$(netstat -lnt | awk '$6 == "LISTEN" && $4 ~ ".$PORT"')" ]; then
		echo "Using random port $PORT"

		# Port not in use. Start SSH socks proxy and record its PID so we can
		# kill it later.
		echo "Starting SSH socks 5 proxy"
        ssh -D $PORT -N $HOST &
        PID=$!

		# Create temp profile and run chrome with the Socks proxy
        BASE_TEMP_DIR=/tmp
        TEMP_DIR=$(mktemp -d $BASE_TEMP_DIR/chrome-socks.XXXXXXX)
		echo "Created temp profile in $TEMP_DIR. Starting browser..."
        $BROWSER_BIN --no-first-run --user-data-dir=$TEMP_DIR --explicitly-allowed-ports=6666 --proxy-server="socks5://localhost:$PORT" $SITES

		# On exit of the browser, kill the Socks proxy, remove temp profile and
		# exit this script
		echo "Browser exited. Killing socks proxy"
        kill $PID
		echo "Socks proxy killed."
		echo "Removing temp profile $TEMP_DIR."
		[ -z "$TEMP_DIR" ] && exit 99 # Safeguard against empty var
		rm -rf "$TEMP_DIR"
        exit 0
    fi
done

