/* Author - Freddie Woods
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

    function fetchLeaderboardCallback(response) {
        document.getElementById("scores").innerHTML = "";
        if (response.status == "0" && response.message != "No Scores") {
            showAlert("error", response.message);
            document.getElementById("scoresError").style.display = "block";
        } else if (response.status == "1" && response.data.length > 0) {
            document.getElementById("scoresError").style.display = "none";
            for (i = 0; i < response.data.length; i ++) {
                var x = document.createElement("LI");
                x.innerHTML = "Rank: "+(i+1)+" "+ "<span class='teamName'>" + response.data[i].TeamName + "</span> " + response.data[i].Letters + " <span class='teamName'> " +"</span>";
                document.getElementById("scores").appendChild(x);
            }
        } else {
            //no game running
            document.getElementById("scoresError").style.display = "block";
        }
    }

    function fetchLeaderboard() {
        HTTPGet("/dashboard/results", fetchLeaderboardCallback);
    }
    setInterval(function(){ fetchLeaderboard(); }, 5000);

    fetchLeaderboard();
}, false);
