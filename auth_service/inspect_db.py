import sqlite3, os
path='auth.db'
print('exists', os.path.exists(path), path)
con=sqlite3.connect(path)
rows=list(con.execute('PRAGMA table_info(user)'))
print(rows)
con.close()