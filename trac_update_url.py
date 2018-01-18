#!/usr/bin/python

import MySQLdb
import MySQLdb.cursors

search = "https://example.nl"
replace = "http://acme.com"

db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="",
    db="trac",
    cursorclass=MySQLdb.cursors.DictCursor
)
cur = db.cursor()
cur_update = db.cursor()

# Search / replace ticket descriptions
cur.execute('SELECT * FROM ticket WHERE description LIKE "%%%s%%"' % (search))
for row in cur:
    description = row["description"].replace(search, replace)
    print "Updating ticket #{}: {}".format(row["id"], row["summary"])
    cur_update.execute("UPDATE ticket SET description = %s WHERE id = %s", (description, row["id"]))
    db.commit()
else:
    print "Tickets: Search text not found"

# Search / replace ticket comments
cur.execute('SELECT * FROM ticket_change WHERE field = "comment" AND newvalue LIKE "%%%s%%"' % (search))
for row in cur:
    newvalue = row["newvalue"].replace(search, replace)
    print "Updating ticket #{}: comment #{}".format(row["ticket"], row["oldvalue"])
    cur_update.execute("UPDATE ticket_change SET newvalue = %s WHERE ticket = %s AND field = %s AND oldvalue = %s", (newvalue, row["ticket"], "comment", row["oldvalue"]))
    db.commit()

# Search / replace wiki contents
cur.execute('''
    SELECT * FROM wiki WHERE (name, version) IN (
	SELECT name, MAX(version) FROM wiki WHERE text LIKE '%%%s%%' GROUP BY (name)
    )
''' % (search), )
for row in cur:
    text = row["text"].replace(search, replace)
    print "Updating wiki page '{}', version {}".format(row["name"], row["version"])
    cur_update.execute("UPDATE wiki SET text = %s WHERE name = %s AND version = %s", (text, row["name"], row["version"]))
    db.commit()

