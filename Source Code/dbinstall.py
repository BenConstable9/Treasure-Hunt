# Author - Ravi Gohel
# Database creation and tables creation

import sqlite3 as sql
import datetime
from Models.adminModel import adminModel

con = sql.connect('Models/treasure.sqlite')
print ("Opened database successfully");

cur = con.cursor()

#Tutors Table
cur.execute('CREATE TABLE IF NOT EXISTS Tutors (TutorID integer PRIMARY KEY AUTOINCREMENT, SubjectID int not null, Name text not null, Room text not null, FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID))')
print ("(1) Tutors Table created successfully");

#Subjects Table
cur.execute('CREATE TABLE IF NOT EXISTS Subjects (SubjectID integer PRIMARY KEY AUTOINCREMENT, SubjectName text not null, Building text not null, GPS text not null)')

#Keepers Table
cur.execute('CREATE TABLE IF NOT EXISTS Keepers (KeeperID integer PRIMARY KEY AUTOINCREMENT, Name text not null, Username text not null UNIQUE, Password text not null, Salt text not null)')
print ("(2) Keepers Table created successfully");

#Games Table
#For 'active', as sqlite3 does not have a boolean data type - 1 will be true and 0 will be false
cur.execute('CREATE TABLE IF NOT EXISTS Games (GameID integer PRIMARY KEY AUTOINCREMENT, SubjectID int not null, GamePin text not null, KeeperID integer not null, Active integer not null, FOREIGN KEY (KeeperID) REFERENCES Keepers (KeeperID), FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID))')
print ("(3) Games Table created successfully");

#Teams Table
cur.execute('CREATE TABLE IF NOT EXISTS Teams (TeamID integer PRIMARY KEY AUTOINCREMENT, TeamName text not null UNIQUE, Subject int not null, GamePin text not null, FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID))')
print ("(4) Teams Table created successfully");

#Results Table
cur.execute('CREATE TABLE IF NOT EXISTS Results (ResultID integer PRIMARY KEY AUTOINCREMENT, TeamID integer not null, StartTime datetime not null, FinishTime datetime, Letters int not null, FOREIGN KEY (TeamID) REFERENCES Teams (TeamID))')
print ("(5) Results Table created successfully");

#Questions Table
cur.execute('CREATE TABLE IF NOT EXISTS Questions (QuestionID integer PRIMARY KEY AUTOINCREMENT, SubjectID int not null, Building text not null, QRLocation text not null, QRText text not null, Question text not null, Answer text not null, GPS text not null, Letter text not null, FOREIGN KEY (SubjectID) REFERENCES Subject(SubjectID))')
print ("(6) Questions Table created successfully");

cur = con.cursor()

adminModel.adminRegister("Test Keeper", "admin", "admin") #Ensures the password will be automatically hashed

con.commit()

cur.close()
