/* Author - Ben Constable
   Handle the dashboard functionality
*/

document.addEventListener('DOMContentLoaded', function(){
    HTTPPost("/dashboard/getLoc", values = "values", addLocationBlocks)

    function addLocationBlocks(response){
      if (response.status == "0") {
          //incorrect response
          showAlert("Unable to load database");
      } else {
          var ul = document.getElementById("Locations");
          var ul2 = document.getElementById("building")

          for (rowNum in response.data){
            var li = document.createElement("li");
            li.id = response.data[rowNum].building
            li.appendChild(document.createTextNode(response.data[rowNum].building));
            ul.appendChild(li);
            var box = document.createElement("input");
            box.id = "letter"+response.data[rowNum].building
            box.className = "finalLoc"
            box.disabled = true;
            box.size = 1;
            ul2.appendChild(box);

          }
    }}

    function verifyLocationCallback(response) {
        if (response.status == "1") {
            document.getElementById("questionBuilding").innerHTML = response.Building;
            document.getElementById("questionText").innerHTML = response.Question;
            document.getElementById("scanModal").style.display = "none";
            document.getElementById("questionAnswerModal").style.display = "block";

            document.forms["questionAnswer"]["questionID"].value = response.QuestionID;
            showAlert("success", response.message);
        } else {
            showAlert("error", response.message);
        }
    }

    /* Fetch the question for the given QR Code */
    function verifyLocation(value) {
        //send off our request
        HTTPPost("/dashboard/verifylocation", "value=" + value, verifyLocationCallback)
    }

    /* Handle the response from answering a question */
    function answerQuestionCallback(response) {
        if (response.status == "0") {
            //incorrect response
            showAlert("questionAnswerModalError", "Incorrect Answer - Try Again");
        } else {
            showAlert("success", "Question Answer Successfully")
            document.getElementById("questionAnswerModal").style.display = "none";
            var ul = document.getElementById("building");
            console.log(response)
            for (rowNum in response.data){
              var box = document.getElementById("letter"+response.data[rowNum].building);
              box.value = response.data[rowNum].letter
              var ul2 = document.getElementById(response.data[rowNum].building);
              ul2.innerHTML = "<del>"+response.data[rowNum].building+"</del>";
            }
            scanner.stop();
            //todo add the letter and cross off the list
            //get the index and add at the correct index
        }
    }

    /* Answer the given question */
    function answerQuestion(e) {
        e.preventDefault();
        //validated the answer
        var answer = document.forms["questionAnswer"]["answer"].value;
        if (answer.length >= 1) {
            //send off our request
            HTTPPost("/dashboard/question", "answer=" + answer + "&questionID=" + document.forms["questionAnswer"]["questionID"].value, answerQuestionCallback)
        } else {
            showAlert("questionAnswerModalError", "Fill In An Answer Before Submitting");
        }
    }

    let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
    scanner.addListener('scan', function (content) {
        //once scanned, send data to verifyLocation
        verifyLocation(content);
    });

    scanner.addListener('active', function (content) {
        document.getElementById("loadingContainer").style.display = "none";
    });

    /*toggles bettween displaying and hiding the scan model*/
    function flipScanModel(e){
        if (document.getElementById("scanModal").style.display === "block"){
            document.getElementById("scanModal").style.display = "none";
            Instascan.Camera.getCameras().then(function (cameras) {
            if (cameras.length > 0) {
                //stop the camera
                scanner.stop();
            } else {
                //give them an error
                showAlert("error", "No Camera Installed - Check Your Settings");
            }
            }).catch(function (e) {
                showAlert("error", e);
            });
        }else{
            document.getElementById("loadingContainer").style.display = "block";
            document.getElementById("scanModal").style.display = "block";
            /* Handles the QR code scanning */
            Instascan.Camera.getCameras().then(function (cameras) {
            if (cameras.length == 1) {
                //always start the first camera
                scanner.start(cameras[0]);
            } else if (cameras.length > 1) {
                //always start the first camera
                scanner.start(cameras[1]);
            } else {
                //give them an error
                showAlert("error", "No Camera Installed - Check Your Settings");
            }
            }).catch(function (e) {
                document.getElementById("loadingContainer").style.display = "none";
                showAlert("error", e);
            });
        }
    }

    /* Handle the closing of a modal
    */
   function closeQuestionAnswerModel(e) {
        e.preventDefault();
        //close it
        document.getElementById("questionAnswerModal").style.display = "none";
    }

    /* Handle opening of a modal
    */
    function openScanModal() {
        //open it
        document.getElementById("scanModal").style.display = "block";
    }

    document.getElementById("closeScanModal").addEventListener("click", flipScanModel);

    document.getElementById("flipScanModel").addEventListener("click", flipScanModel);

    document.forms["questionAnswer"]["cancel"].addEventListener("click", closeQuestionAnswerModel);

    document.forms["questionAnswer"]["submit"].addEventListener("click", answerQuestion);
});
