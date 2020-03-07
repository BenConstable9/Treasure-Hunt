from Models.gameModel import gameModel
import dbinstall

class TestGameModel:

    """Test Create Game"""
    def testCreateGame(self):
        response = gameModel.createGame("1", "1");
        assert response["status"] == "1"
        #check that there is only one game
        response = gameModel.getGames("1", "1")
        assert len(response) == 1

    """Test Create Game When Already Existing Game"""
    def testCreateGameError(self):
        response = gameModel.createGame("1", "1");
        assert response["message"] == "You already have a game running."

    """Test getting the active games a keeper has"""
    def testGetGames(self):
        #end all games
        gameModel.endGame("1")
        #get new games and compare the results
        game = gameModel.createGame("1", "1");
        response = gameModel.getGames("1", "1")
        assert response[0]["GamePin"] == str(game["GamePin"])

    """Test getting a list of inactive games"""
    def testGetGamesInactive(self):
        response = gameModel.getGames("1", "")
        assert len(response) > 0

    """Test the ending of the game"""
    def testEndGame(self):
        response = gameModel.getGames("1", "1")
        assert len(response) == 1
        #now end the game
        gameModel.endGame("1")
        #check that there are now no games
        response = gameModel.getGames("1", "1")
        assert len(response) == 0