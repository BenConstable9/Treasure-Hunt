# Author - Ravi Gohel - modified by Zach Lavender
# Database creation and tables creation

import sqlite3 as sql
import datetime
from Models.adminModel import adminModel

con = sql.connect('Models/treasure.sqlite')
print ("Opened database successfully");

cur = con.cursor()

#Tutors Table
cur.execute('CREATE TABLE IF NOT EXISTS Tutors (TutorID integer PRIMARY KEY AUTOINCREMENT, SubjectID int not null, Name text not null, Room text not null, FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID))')
print ("(1) Tutors Table created successfully");

#Subjects Table
cur.execute('CREATE TABLE IF NOT EXISTS Subjects (SubjectID integer PRIMARY KEY AUTOINCREMENT, SubjectName text not null, Building text not null, GPS text not null)')
print ("(2) Subjects Table created successfully")

#Keepers Table
cur.execute('CREATE TABLE IF NOT EXISTS Keepers (KeeperID integer PRIMARY KEY AUTOINCREMENT, Name text not null, Username text not null UNIQUE, Password text not null, Salt text not null)')
print ("(3) Keepers Table created successfully");

#Games Table
    #For 'active', as sqlite3 does not have a boolean data type - 1 will be true and 0 will be false
cur.execute('CREATE TABLE IF NOT EXISTS Games (GameID integer PRIMARY KEY AUTOINCREMENT, SubjectID int not null, GamePin text not null, KeeperID integer not null, Active integer not null, FOREIGN KEY (KeeperID) REFERENCES Keepers (KeeperID), FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID))')
print ("(4) Games Table created successfully");

#Teams Table
cur.execute('CREATE TABLE IF NOT EXISTS Teams (TeamID integer PRIMARY KEY AUTOINCREMENT, TeamName text not null UNIQUE, SubjectID int not null, GamePin text not null, FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID))')
print ("(5) Teams Table created successfully");

#Results Table
cur.execute('CREATE TABLE IF NOT EXISTS Results (ResultID integer PRIMARY KEY AUTOINCREMENT, TeamID integer not null, StartTime datetime not null, FinishTime datetime, Letters int not null, FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("(6) Results Table created successfully");

#Questions Table
cur.execute('CREATE TABLE IF NOT EXISTS Questions (QuestionID integer PRIMARY KEY AUTOINCREMENT, SubjectID int not null, Building text not null, QRLocation text not null, QRText text not null, Question text not null, Answer text not null, GPS text not null, Letter text not null, FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID))')
print ("(7) Questions Table created successfully");

cur = con.cursor()

adminModel.adminRegister("Test Keeper", "admin", "admin") #Ensures the password will be automatically hashed
# Insert the team data
cur.execute("INSERT INTO Subjects (SubjectName,Building,GPS) VALUES ('Computer Science', 'Harrison', '123456')")
cur.execute("INSERT INTO Subjects (SubjectName,Building,GPS) VALUES ('Psychology', 'Washington Singer', '123431')")
cur.execute("INSERT INTO Teams (TeamName,GamePin,SubjectID) VALUES ('RaviGGG', '123',1)")
cur.execute("INSERT INTO Games (SubjectID,GamePin,KeeperID,Active) VALUES ('1', '123',1,1)")
cur.execute("INSERT INTO Tutors (SubjectID,Name,Room) VALUES (1, 'Ronaldo Menezes', '007')")
cur.execute("INSERT INTO Tutors (SubjectID,Name,Room) VALUES (1, 'Chunbo Luo', '131')")
cur.execute("INSERT INTO Tutors (SubjectID,Name,Room) VALUES (1, 'David Wakeling', '004')")
cur.execute("INSERT INTO Tutors (SubjectID,Name,Room) VALUES (2, 'Mitch Berger', '5235')")
con.commit()

cur.close()
