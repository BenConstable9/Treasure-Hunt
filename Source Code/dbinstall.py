import sqlite3

conn = sqlite3.connect('treasure.db')
print "Opened database successfully";

conn.execute('CREATE TABLE Teams ()')
print "Table created successfully";
conn.close()
