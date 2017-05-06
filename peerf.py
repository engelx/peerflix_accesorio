#!/usr/bin/python

import urllib
import sqlite3
import sys
import subprocess
import pygtk
pygtk.require('2.0')
import gtk

conn = sqlite3.connect('trackers')
c = conn.cursor()

clp = gtk.clipboard_get()
url = clp.wait_for_text()

if url[:8] != "magnet:?":
	print "no magnet in clipboard"
	sys.exit()


url = url.split("&")

stringout = ""

for i in url:
	url2 = i.split("=")
	if url2[0] == "tr":
		tr = urllib.unquote(url2[1]).decode('utf8')
		sql = "SELECT id FROM trackers WHERE tracker='{}'".format(tr)
		c.execute(sql)
		if len(c.fetchall()) == 0:
			print "inserted"
			sql = "INSERT INTO trackers (tracker) VALUES('{}')".format(tr)
			c.execute(sql)
	else:
		stringout += i+"&"

conn.commit()

sql = "SELECT tracker FROM trackers"

trackers = []
for t in c.execute(sql):
	trackers.append("td="+urllib.quote_plus(t[0]))

print len(trackers), " trackers loaded"

trackers = "&".join(trackers)
cmd = "peerflix \""+ stringout+trackers + "\" --vlc -d"

p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
 
try:
	while True:
	    out = p.stderr.read(1)
	    if out == '' and p.poll() != None:
	        break
	    if out != '':
	        sys.stdout.write(out)
	        sys.stdout.flush()
	print 'terminado'
except KeyboardInterrupt:
	print 'cancelado'
	
	
print stringout
print '-----------'