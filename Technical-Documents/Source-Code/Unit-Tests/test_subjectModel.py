from Models.subjectModel import subjectModel
from Models.gameModel import gameModel
import dbinstall

class TestSubjectModel:
    """Test Create Subjects"""
    def testCreateSubject(self):
        response = subjectModel.createSubject("Computer Science", "Harrison", "50.737806", "-3.532618")
        assert response["status"] == "1"

    """Test Create Subjects Duplicate"""
    def testCreateSubjectError(self):
        response = subjectModel.createSubject("Computer Science", "Harrison", "50.737806", "-3.532618")
        assert response["status"] == "0"

    """Test Get Subjects"""
    def testGetSubjects(self):
        response = subjectModel.getSubjects()
        assert response["status"] == "1"

    """Test Verify Pin"""
    def testVerifyPin(self):
        gameModel.endGame("1")
        game = gameModel.createGame("1", "1")
        response = subjectModel.verifyPin(str(game["GamePin"]))
        assert response["subject"] == "Computer Science"

    """Test Get Building"""
    def testGetBuilding(self):
        response = subjectModel.getBuilding("1")
        assert response["building"] == "Harrison"