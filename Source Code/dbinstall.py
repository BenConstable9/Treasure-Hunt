import sqlite3 as sql
import datetime

con = sql.connect('Models/treasure.sqlite')
print ("Opened database successfully");

cur = con.cursor()

#Tutors Table
cur.execute('CREATE TABLE IF NOT EXISTS Tutors (TutorID integer PRIMARY KEY AUTOINCREMENT, Subject text not null, Name text not null, Room int not null)')
print ("Table created successfully");

#Keepers Table
cur.execute('CREATE TABLE IF NOT EXISTS Keepers (KeeperID integer PRIMARY KEY AUTOINCREMENT, Name text not null, Username text not null UNIQUE, Password text not null, Salt text not null)')
print ("Table created successfully");

#Games Table
    #For active, as sqlite3 does not have a boolean data type - 1 will be true and 0 will be false
cur.execute('CREATE TABLE IF NOT EXISTS Games (GameID integer PRIMARY KEY AUTOINCREMENT, Subject text not null, GamePin text not null, KeeperID integer not null, Active integer not null, FOREIGN KEY (KeeperID) REFERENCES Keepers (KeeperID))')
print ("Table created successfully");

#Teams Table
cur.execute('CREATE TABLE IF NOT EXISTS Teams (TeamID integer PRIMARY KEY AUTOINCREMENT, TeamName text not null UNIQUE, Subject text not null, GamePin text not null)')
print ("Table created successfully");

#Results Table
cur.execute('CREATE TABLE IF NOT EXISTS Results (ResultID integer PRIMARY KEY AUTOINCREMENT, TeamID integer not null, StartTime datetime not null, FinishTime datetime, Letters int not null, FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("Table created successfully");

#Questions Table
cur.execute('CREATE TABLE IF NOT EXISTS Questions (QuestionID integer PRIMARY KEY AUTOINCREMENT, Subject text not null, Location text not null, QRLocation text not null, QRtext text not null, Question text not null, Answer text not null, GPS text not null, Letter text not null)')
print ("Table created successfully");

cur = con.cursor()

cur.execute("INSERT INTO Keepers VALUES(null,'Ravi','RaviUsername','Test','Salt') ")
cur.execute("INSERT INTO Games VALUES(null,'Computer Science','123', 1, 1) ")

cur.execute("SELECT * FROM Games")

game = cur.fetchall()

print("test 1")

print(game)

cur.execute("SELECT * FROM Keepers")

game = cur.fetchall()

print("test 1")

print(game)

con.commit()


cur.close()
