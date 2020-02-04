import sqlite3 as sql
import datetime

conn = sql.connect('treasure.db')
print ("Opened database successfully");

#Tutors Table
conn.execute('CREATE TABLE IF NOT EXISTS Tutors (TutorID integer PRIMARY KEY AUTOINCREMENT, Subject text not null, Name text not null, Room int not null)')
print ("Table created successfully");

#Keepers Table
conn.execute('CREATE TABLE IF NOT EXISTS Keepers (KeeperID integer PRIMARY KEY AUTOINCREMENT, Name text not null, Username text not null UNIQUE, Password text not null, Salt text not null)')
print ("Table created successfully");

#Games Table
    #For active, as sqlite3 does not have a boolean data type - 1 will be true and 0 will be false
conn.execute('CREATE TABLE IF NOT EXISTS Games (GameID integer PRIMARY KEY AUTOINCREMENT, Subject text not null, GamePin integer not null, Issuer integer not null, Active integer not null)')
print ("Table created successfully");

#Teams Table
conn.execute('CREATE TABLE IF NOT EXISTS Teams (TeamID integer PRIMARY KEY AUTOINCREMENT, TeamName text not null UNIQUE, Subject text not null, GamePin integer not null)')
print ("Table created successfully");

#Results Table
conn.execute('CREATE TABLE IF NOT EXISTS Results (ResultID integer PRIMARY KEY AUTOINCREMENT, TeamID integer not null, StartTime datetime not null, FinishTime datetime, Letters int not null, FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("Table created successfully");

#Questions Table
conn.execute('CREATE TABLE IF NOT EXISTS Questions (QuestionID integer PRIMARY KEY AUTOINCREMENT, Subject text not null, Location text not null, QRLocation text not null, QRtext text not null, Question text not null, Answer text not null, GPS text not null, Letter text not null)')
print ("Table created successfully");
conn.close()
