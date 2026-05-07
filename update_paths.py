import os
import sqlite3

DB_PATH = "nceltt.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT evidence_id, file_path FROM evidence")
rows = cur.fetchall()
for id_, fp in rows:
    if not fp:
        continue
    fname = os.path.basename(fp)
    cur.execute("UPDATE evidence SET file_path = ? WHERE evidence_id = ?", (fname, id_))

conn.commit()
conn.close()