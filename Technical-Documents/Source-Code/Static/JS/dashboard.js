/* Author - Ben Constable
   Handle the dashboard functionality
*/

document.addEventListener('DOMContentLoaded', function(){
    let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
    scanner.addListener('scan', function (content) {
        verifyLocation(content);
    });
    Instascan.Camera.getCameras().then(function (cameras) {
        if (cameras.length > 0) {
            scanner.start(cameras[0]);
        } else {
            showAlert("error", "No Camera Installed");
        }
    }).catch(function (e) {
        showAlert("error", e);
    });

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

    /* Handle the closing of a modal
    */
   function closeScanModal(e) {
        e.preventDefault();
        //close it
        document.getElementById("scanModal").style.display = "none";
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

    document.getElementById("closeScanModal").addEventListener("click", closeScanModal);

    document.getElementById("openScanModal").addEventListener("click", openScanModal);

    document.forms["questionAnswer"]["cancel"].addEventListener("click", closeQuestionAnswerModel);
});