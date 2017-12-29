#!/usr/bin/python

import sys
import gzip
import re
import os

#
# Configuration
#
# Only count any files with these extensions as 'pages'.
page_exts = ['.php', '.html', '.pdf', '']
page_ignore = ['.png', '.gif', '.jpg', '.css', '.ico']

#
# Handle commandline options
#
def usage():
    print "apache_stats: Simple Apache log analyser"
    print
    print "Usage: apache_stats LOGFILE [LOGFILE].."

if len(sys.argv) < 2:
    usage()
    sys.exit(1)

logfiles = sys.argv[1:]

# Apache Combined logfile format regular expression parsing thingymajig
re_xsline = x = re.compile('(.*) (.*) (.*) \[(.*)\] "(.*) (.*) (.*)" ([0-9]*) (.*) "(.*)" "(.*)"')

served_total = 0
served_pages = 0
date_first = None
date_last = None
visitor_unique = {}
pages_mostvisit = {}
referers = {}

for logfile in logfiles:
    if logfile.endswith('.gz'):
        f = gzip.open(logfile, 'r')
    else:
        f = file(logfile, 'r')

    for line in f:
        try:
            t1 = line.split('"')
            remotehost, ident, uid, date = t1[0].split(' ', 3)
            method, url, protocol = t1[1].split(' ', 2)
            rescode, bsent = t1[2].strip().split(' ', 1)
            referer = t1[3]
            uagent = t1[5]
            date = date[1:-2]

            served_total += 1
            ext = os.path.splitext(url)[1]
            if not ext in page_ignore:
                for ext in page_exts:
                    if url.endswith(ext):
                        served_pages += 1
                        pages_mostvisit[url] = pages_mostvisit.get(url, 0) + 1
                        break
                if '.' not in url:
                    served_pages += 1
                if not date_first or date < date_first:
                    date_first = date
                if not date_last or date > date_last:
                    date_last = date
                visitor_unique[remotehost] = 1
                if 'electricmonk' not in referer and 'google' not in referer and referer[-1] != '/':
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
for k, v in sorted([(v, k) for k, v in pages_mostvisit.items()])[-30:]:
    print "\t", k, v
print "Top 20 Referers"
for k, v in sorted([(v, k) for k, v in referers.items()])[-30:]:
    print "\t", k, v
