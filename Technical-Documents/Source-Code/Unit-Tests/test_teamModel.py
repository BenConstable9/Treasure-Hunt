from Models.teamModel import teamModel
from Models.gameModel import gameModel
import dbinstall

class TestTeamModel:
    """Test Register Team"""
    def testRegisterTeam(self):
        #create a new game
        gameModel.endGame("1")
        game = gameModel.createGame("1", "1");

        #try registering
        response = teamModel.registerTeam("Test Team", game["GamePin"], "1")
        assert response["message"] == "Team Registration Successfull"

        #now try again with the same team name
        response = teamModel.registerTeam("Test Team", game["GamePin"], "1")
        assert response["message"] == "Team Registration Unsuccessful - Team Name Already Taken"

    """Test Register Team with an invalid GamePin"""
    def testRegisterTeamGamePinError(self):
        response = teamModel.registerTeam("Test Team3", "1", "1")
        assert response["message"] == "Team Registration Unsuccessful - Game Pin Invalid"

    """Test Register Team With Empty Tutor"""
    def testRegisterTeamTutorError(self):
        #create a new game
        gameModel.endGame("1")
        game = gameModel.createGame("1", "1");

        #try registering
        response = teamModel.registerTeam("Test Team", game["GamePin"], "None")
        assert response["message"] == "Team Registration Unsuccessful - Tutor is empty."

    """Test Register Team With Empty Name"""
    def testRegisterTeamNameError(self):
        #create a new game
        gameModel.endGame("1")
        game = gameModel.createGame("1", "1");

        #try registering
        response = teamModel.registerTeam("", game["GamePin"], "1")
        assert response["message"] == "Team Registration Unsuccessful -  Team Name is empty - "

    """Test Team Logging In"""
    def testLoginTeam(self):
        #create a new game
        gameModel.endGame("1")
        game = gameModel.createGame("1", "1");

        #try registering
        response = teamModel.registerTeam("Test Login Team", game["GamePin"], "1")
        assert response["message"] == "Team Registration Successfull"

        #now try logging in
        response = teamModel.loginTeam("Test Login Team", game["GamePin"])
        assert response["message"] == "Team Logged In Successfully"

    """Test Team Logging In With Invalid Game Pin"""
    def testLoginTeamError(self):
        #create a new game
        gameModel.endGame("1")
        game = gameModel.createGame("1", "1");

        #try registering
        response = teamModel.registerTeam("Test Login Error Team", game["GamePin"], "1")
        assert response["message"] == "Team Registration Successfull"

        #now try logging in
        response = teamModel.loginTeam("Test Login Error Team", "1")
        assert response["message"] == "Team Logging In Unsuccessful - Invalid Game Pin"