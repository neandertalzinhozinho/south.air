import sqlite3, json, datetime
db = r'C:\Users\tromb\.local\share\opencode\opencode.db'
c = sqlite3.connect('file:' + db.replace('\\','/') + '?mode=ro', uri=True)
c.row_factory = sqlite3.Row
print("=== RECENT SESSIONS ===")
for r in c.execute("select id,parent_id,title,agent,time_created,time_updated from session_v2 order by time_updated desc limit 40"):
    print(dict(r))
print("=== RECENT JOBS ===")
for r in c.execute("select id,session_id,child_session_id,kind,title,status,time_created from job order by time_created desc limit 30"):
    print(dict(r))
