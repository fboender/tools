#!/bin/sh

while [ -n "$1" ]; do
	JAR=$1
	JAD="`basename \"$JAR\" .jar`.jad"
	JAR_SIZE=`du -b "$1" | cut -f1`

	echo -n "Generating \"$JAD\" from \"$JAR\".. "
	unzip -p -x "$1" META-INF/MANIFEST.MF > "$JAD"
	echo "" >> "$JAD"
	echo "MIDlet-Jar-URL: $1" >> "$JAD"
	echo "MIDlet-Jar-Size: $JAR_SIZE" >> "$JAD"
	echo "Done."

	shift
done
