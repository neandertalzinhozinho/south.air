import sqlite3, json, sys, os
db = r'C:\Users\tromb\.local\share\opencode\opencode.db'
c = sqlite3.connect('file:' + db.replace('\\','/') + '?mode=ro', uri=True)
for (name,) in c.execute("select name from sqlite_master where type='table' order by name"):
    print('TABLE', name)
    print('  cols:', [r[1] for r in c.execute('pragma table_info("%s")' % name)])
