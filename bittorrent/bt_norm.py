#!/usr/bin/python

import optparse
import os
import re
import sys
import shutil

base_path = '/storage/tvseries/'
down_path = '/home/todsah/download'

patterns_epi = [
	'(?P<series>.*)[sS](?P<season>\d+?)[eE](?P<episode>\d+)',
	'(?P<series>.*)(?P<season>\d\d)(?P<episode>\d\d)',
	'(?P<series>.*)(?P<season>\d)(?P<episode>\d\d)',
	'(?P<series>.*)(?P<season>\d)x(?P<episode>\d\d)',
]

# Handle options
parser = optparse.OptionParser(
	usage="%prog [OPTIONS] [download path]",
	version="%prog 0.1",
	description='Find downloaded TV series torrent files and normale/move them.')

parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help="Do not actually do anything.")

(options, args) = parser.parse_args()
if args:
	down_path = args.pop(0)

sys.stdout.write('Searching in %s\n' % (down_path))

for fname in [fname for fname in os.listdir(down_path) if os.path.splitext(fname)[1] == '.avi']:
	# Try to find info in a fuzzy way.
	matches = []
	for pattern in patterns_epi:
		m = re.match(pattern, fname)
		if m:
			matches.append(m.groupdict())
	# See which matches the best
	info = None
	best_score = -1
	for match in matches:
		score = 0
		if int(match['episode']) != 0: score += 1
		if int(match['season']) != 0: score += 1
		if score > 0 and score > best_score:
			info = match
			best_score = score

	if not info:
		sys.stderr.write('Couldn\'t find match for: %s\n' % (fname))
		continue

	# Normalize the series name
	info['series'] = info['series'].replace('.', ' ')
	info['series'] = info['series'].replace('_', ' ')
	info['series'] = ' '.join([s.capitalize() for s in info['series'].split(' ')])
	info['series'] = info['series'].strip()

	# Normalize season, episode
	info['season'] = int(info['season'])
	info['episode'] = int(info['episode'])

	# Build final paths
	season_path = os.path.join(base_path, str(info['series']), 'Season %s' % (str(info['season'])))
	file_path = os.path.join(season_path, '%s - S%02i E%02i.avi' % (info['series'], info['season'], info['episode']))

	# SOme checks
	if not os.path.exists(base_path):
		sys.stderr.write('Base path %s does not exist. Aborting.\n' % (base_path))
		sys.exit(1)
	else:
		sys.stdout.write('%s -> %s\n' % (fname, file_path))
		if not options.dryrun:
			try:
				os.makedirs(season_path)
			except OSError, e:
				if e.errno == 17:
					# File exists
					pass 
				else:
					raise e
			shutil.move(os.path.join(down_path, fname), file_path)
