/* Author - Freddie Woods
*/

document.addEventListener('DOMContentLoaded', function(){
  /* Handle the callback from creating the leaderboard

  :param reponse: the response from the request
  */
    function fetchLeaderboardCallback(response) {
        document.getElementById("scores").innerHTML = "";
        //if error or no scores the show error
        if (response.status == "0" && response.message != "No Scores") {
            showAlert("error", response.message);
            document.getElementById("scoresError").style.display = "block";
        } else if (response.status == "1" && response.data.length > 0) {
            //if no error then don't display anything.
            document.getElementById("scoresError").style.display = "none";
            sortedResponse = sorted(reponse.data,key=lambda x:[2] )
            for (i = 0; i < response.data.length; i ++) {
                var x = document.createElement("LI");
                //outputs the data in a list view.
                x.innerHTML = "Rank: <b>"+(i+1)+"</b> "+ "| <span class='teamName'>" + response.data[i].TeamName + "</span> | Letters: <b>" + response.data[i].Letters + "</b><span class='teamName'> | StartTime: <b>" + response.data[i].StartTime +"</b><span class='teamName'>"+"</span>";
                document.getElementById("scores").appendChild(x);
            }
        } else {
            //no game running
            document.getElementById("scoresError").style.display = "block";
        }
    }

    //Obtains the scores from the webpage which stores the data.
    function fetchLeaderboard() {
        HTTPGet("/dashboard/results", fetchLeaderboardCallback);
    }

    //Calls fetchLeaderboard every 5 seconds to update the data.
    setInterval(function(){ fetchLeaderboard(); }, 5000);

    fetchLeaderboard();
}, false);
