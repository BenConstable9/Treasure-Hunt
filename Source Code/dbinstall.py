import sqlite3 as sql
import datetime

conn = sql.connect('treasure.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Users (UserID integer PRIMARY KEY, TeamID int not null, Name string not null, FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("Table created successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Teams (TeamID int PRIMARY KEY, TeamName string not null UNIQUE, Password string not null, Subject string not null)')
print ("Table created successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Results (ResultID int PRIMARY KEY, ClueID int not null, TeamID int not null, Result string not null, TimeTaken datetime not null, FOREIGN KEY (ClueID) REFERENCES Clue (ClueID), FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("Table created successfully");

conn.execute('CREATE TABLE IF NOT EXISTS Clues (ClueID int PRIMARY KEY, Subject string not null, Question string not null, Hint string not null, Answer string not null)')
print ("Table created successfully");
conn.close()
