#!/usr/bin/python

import os
import re

basepath = '/storage/tvseries'
for series in sorted(os.listdir(basepath)):
	serie_epi = []
	for dirpath, dirnames, filenames in os.walk(os.path.join(basepath, series)):
		serie_epi += [os.path.join(dirpath, filename) for filename in filenames]
	serie_epi.sort(lambda a, b: cmp(a.lower(), b.lower()))
	
	final_epi = os.path.basename(serie_epi[-1])
	print "%s: %s" % (series, final_epi) 
