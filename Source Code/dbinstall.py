import sqlite3 as sql
import datetime

conn = sql.connect('treasure.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Users (UserID integereger PRIMARY KEY AUTOINCREMENT, TeamID integer not null, Name string not null, FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("Table created successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Teams (TeamID integer PRIMARY KEY AUTOINCREMENT, TeamName string not null UNIQUE, Password string not null, Subject string not null)')
print ("Table created successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Results (ResultID integer PRIMARY KEY AUTOINCREMENT, ClueID integer not null, TeamID integer not null, Result string not null, TimeTaken datetime not null, FOREIGN KEY (ClueID) REFERENCES Clue (ClueID), FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("Table created successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Clues (ClueID integer PRIMARY KEY AUTOINCREMENT, Subject string not null, Question string not null, Hinteger string not null, Answer string not null)')
print ("Table created successfully");
conn.close()
