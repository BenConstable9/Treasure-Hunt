/* Author - Adam Bannister
*/

document.addEventListener('DOMContentLoaded', function(){
  /* Handle the callback from creating the leaderboard

  :param reponse: the response from the request
  */
  function createLeaderboardCallback(response) {
    if (response.status == "1") {
      console.log(response)
    }
  }

  HTTPGet("/dashboard/leaderboard/data", createLeaderboardCallback)
});
