from pathlib import Path
import sqlite3, sys
p=Path('db.sqlite3')
if not p.exists():
    print('MISSING')
    sys.exit(0)
print('path', p.resolve())
print('size', p.stat().st_size)
b=p.read_bytes()[:16]
print('header_bytes', b)
print('is_sqlite', b.startswith(b'SQLite format 3'))
try:
    conn=sqlite3.connect('db.sqlite3')
    cur=conn.cursor()
    cur.execute('PRAGMA integrity_check;')
    print('integrity_check', cur.fetchone())
    conn.close()
except Exception as e:
    print('SQLITE_ERROR', e)
