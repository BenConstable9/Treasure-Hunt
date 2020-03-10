from Models.questionModel import questionModel
from Models.gameModel import gameModel
from Models.subjectModel import subjectModel
from Models.teamModel import teamModel
import dbinstall

class TestQuestionModel:

    """Test Create A Question"""
    def testCreateQuestion(self):
        subject = subjectModel.createSubject("Test Subject", "Harrison", "50.737806", "-3.532618")
        response = questionModel.createQuestion(subject["ID"], "Test Building", "Wall", "Contents", "Test Question", "Answer", "T", "0", "123.00", "123.00")

        assert response["status"] == "1"

    """Test Create A Question With Invalid Subject"""
    def testCreateQuestionError(self):
        response = questionModel.createQuestion("10", "Test Building", "Wall", "Contents", "Test Question", "Answer", "T", "0", "123.00", "123.00")

        assert response["message"] == "Question Creation Unsuccessful - Subject Not In DB"

    """Test Verifying Location"""
    def testVerifyLocation(self):
        subject = subjectModel.createSubject("Test Subject 2", "Harrison", "50.737806", "-3.532618")
        response = questionModel.createQuestion(subject["ID"], "Test Building", "Wall", "Contents", "Test Question", "Answer", "T", "0", "123.00", "123.00")
        response = questionModel.verifyLocation(subject["ID"], "Contents")

        assert response["Question"] == "Test Question"

    """Test Verifying Location with invalid QR text"""
    def testVerifyLocation(self):
        subject = subjectModel.createSubject("Test Subject 3", "Harrison", "50.737806", "-3.532618")
        response = questionModel.createQuestion(subject["ID"], "Test Building", "Wall", "Contents", "Test Question", "Answer", "T", "0", "123.00", "123.00")
        response = questionModel.verifyLocation(subject["ID"], "WrongText")

        assert response["message"] == "Invalid QR Code - try scanning again."

    """Test Getting Questions"""
    def testGetQuestions(self):
        subject = subjectModel.createSubject("Test Subject 4", "Harrison", "50.737806", "-3.532618")
        questionModel.createQuestion(subject["ID"], "Test Building", "Wall", "Contents", "Test Question", "Answer", "T", "0", "123.00", "123.00")

        #now get the subjects
        response = questionModel.getQuestions(subject["ID"])

        assert len(response["data"]) > 0

    """Test checking answer"""
    def testCheckAnswer(self):
        subject = subjectModel.createSubject("Test Subject 5", "Harrison", "50.737806", "-3.532618")
        question = questionModel.createQuestion(subject["ID"], "Test Building", "Wall", "Contents", "Test Question", "Answer", "T", "0", "123.00", "123.00")
        print(question)

        #create game and team
        game = gameModel.createGame("1", subject["ID"]);
        team = teamModel.registerTeam("Question Test", game["GamePin"], "1")
        print(team)

        response = questionModel.checkAnswer("Answer",question["ID"],team["ID"])

        assert response["data"][0]["building"] == "Test Building"