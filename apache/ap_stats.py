#!/usr/bin/python

import sys
import re 

re_xsline = x = re.compile('(.*) (.*) (.*) \[(.*)\] "(.*) (.*) (.*)" ([0-9]*) (.*) "(.*)" "(.*)"')

page_exts = ['.php', '.html', '.pdf']

served_total = 0
served_pages = 0
date_first = None
date_last = None
visitor_unique = {}
pages_mostvisit = {}
referers = {}

for line in file('access.log', 'r'):
	try:
		t1 = line.split('"')
		remotehost, ident, uid, date = t1[0].split(' ', 3)
		method, url, protocol = t1[1].split(' ', 2)
		rescode, bsent = t1[2].strip().split(' ', 1)
		referer = t1[3]
		uagent = t1[5]
		date = date[1:-2]

		served_total += 1
		for ext in page_exts:
			if url.endswith(ext):
				served_pages += 1
				break
		if '.' not in url:
			served_pages += 1
		if not date_first:
			date_first = date
		date_last = date
		visitor_unique[remotehost] = 1
		pages_mostvisit[url] = pages_mostvisit.get(url, 0) + 1
		if 'electricmonk' not in referer:
			referers[referer] = referers.get(referer, 0) + 1
	except Exception, e:
		pass

print "Stats"
print "\tFrom:            %10s" % (date_first)
print "\tTo:              %10s" % (date_last)
print "\tTotal served:    %10s" % (served_total)
print "\tPages served:    %10s" % (served_pages)
print "\tUnique visitors: %10s" % (len(visitor_unique))
print "Top 20 URLs"
for k, v in sorted([(v, k) for k, v in pages_mostvisit.items()])[-20:]:
	print "\t", k, v
print "Top 20 Referers"
for k, v in sorted([(v, k) for k, v in referers.items()])[-20:]:
	print "\t", k, v
