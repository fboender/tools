#!/usr/bin/env python

import os

src = '/storage/tvseries,/storage/movies/'
dst = '/storage/tvseries/latest/'
nr = 20

def walker(dirname, files = []):
	for dirpath, dirnames, filenames in os.walk(dirname):
		for filename in filenames:
			if not os.path.islink(os.path.join(dirpath, filename)):
				st = os.stat(os.path.join(dirpath, filename))
				files.append( (st.st_ctime, dirpath, filename) )

files = []
for dirname in src.split(','):
	walker(dirname, files)
files.sort()
for filename in os.listdir(dst):
	os.unlink(os.path.join(dst, filename))
cnt = 0
for file in files[-nr:]:
	cnt += 1
	dst_fname = os.path.join(dst, '%05i - %s' % (cnt, file[2]))
	os.symlink(os.path.join(file[1], file[2]), dst_fname)
