from Models.tutorModel import tutorModel
from Models.gameModel import gameModel
import dbinstall

class TestTutorModel:
    """Test Create Tutor"""
    def testCreateTutor(self):
        response = tutorModel.createTutor("1", "Test Tutor", "101")
        assert response["status"] == "1"

    """Test Obtain Tutors"""
    def testObtainTutors(self):
        response = tutorModel.obtainTutors("1")
        assert response["tutorNames"][0] == "Test Tutor"
        