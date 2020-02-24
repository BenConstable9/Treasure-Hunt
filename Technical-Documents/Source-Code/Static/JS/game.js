/* Author - Ben Constable
   Modified - Ravi Gohel
   Handle the ajax functions for creating and uploading games
*/

document.addEventListener('DOMContentLoaded', function(){
    /* Handle the callback from creating a game

        :param response: The response from the request
    */
    function createGameCallback(response) {
        if (response.status == "1") {
            //add the game pin
            document.getElementById('gamePin').value = "Current Game Pin: " + response.GamePin;

            //stop them creating more games
            creates = document.getElementsByClassName('createGameButton');
            for (i = 0; i < creates.length; i ++) {
                creates[i].disabled = true;
            }

            //display message
            showAlert("success", response.message);
            document.getElementById("endGame").disabled = false;
        } else {
            showAlert("error", response.message);
        }
    }

    /* Send off a request to create a new game
    */
    function createGame() {
        //get the json object
        subjectID = JSON.parse(this.dataset.json.replace(/'/g, '"')).SubjectID;

        //send the request
        var params = "SubjectID=" + subjectID;
        HTTPPost("/admin/game/create", params, createGameCallback)
    }

    /* Handle the callback from ending a game

        :param response: The response from the request
    */
    function endGameCallback(response) {
        if (response.status == "1") {
            //let the users use the buttons again
            document.getElementById('gamePin').value = "No Game Running";
            creates = document.getElementsByClassName('createGameButton');
            for (i = 0; i < creates.length; i ++) {
                creates[i].disabled = false;
            }

            //show message
            showAlert("success", response.message);
            document.getElementById("endGame").disabled = true;
        } else {
            showAlert("error", response.message);
        }
    }

    /* Handle the callback from ending a game

        :param response: The response from the request
    */
    function logoutCallback(response) {
        if (response.status == "1"){
          window.location.replace("/admin");

        }
    }

    /* Send off a request to end a game

        :param response: The response from the request
    */
    function endGame() {
        HTTPPost("/admin/game/end", "", endGameCallback)
    }

    /* Send off a request to log the user out
        :param response: The response from the request
    */
    function logout() {
        HTTPPost("/admin/game/logout", "", logoutCallback)
    }

    /* Handle the callback from uploading a game

        :param response: The response from the request
    */
    function handleUploadCallback(response) {
        if (response.status == "1") {
            showAlert("success", response.message);

            //make the error disappear
            if (document.getElementById('noConfigError')) {
                document.getElementById('noConfigError').style.display = "none";
            }
            var table = document.getElementById("configTable");
            table.style.display = "table";

            //add a new row to the table
            var row = table.getElementsByTagName('tbody')[0].insertRow(0);

            //convert to a format to store
            buttonJSON = JSON.stringify(response);

            //add the cells
            row.insertCell(0).innerHTML = response.SubjectID;
            row.insertCell(1).innerHTML = response.SubjectName;
            row.insertCell(2).innerHTML = response.Building;
            row.insertCell(3).innerHTML = '<button id="create' + response.SubjectID + '" class="createGameButton">Create Game</button>';
            row.insertCell(4).innerHTML = '<button id="print' + response.SubjectID + '" class="printQRCode">Print QR Codes</button>';

            //add the event listeners
            document.getElementById('create' + response.SubjectID).addEventListener("click", createGame);
            document.getElementById('create' + response.SubjectID).dataset.json = buttonJSON;
            //todo add the event listener for the generateqr code
        } else {
            showAlert("error", response.message);
        }
    }

    /* Handle the submission of the game form
    */
    function handleUpload(e) {
        //stop a page reload
        e.preventDefault();

        //create the form data and send it off
        var form = document.forms["configUpload"];
        var formData = new FormData();
        formData.append("file", form["file"].files[0]);

        HTTPUploadFile("/admin/upload", formData, handleUploadCallback);
    }

    /* Handle the closing of a modal
    */
    function closeConfigModal(e) {
        e.preventDefault();
        //close it
        document.getElementById("configModal").style.display = "none";
    }

    /* Handle opening of a modal
    */
    function openConfigModal() {
        //close registerAdminModel if opening
        document.getElementById("registerAdminModel").style.display = "none";
        document.getElementById("changePasswordModel").style.display = "none";
        //open it
        document.getElementById("configModal").style.display = "block";
    }

    /* Handle the closing of a modal
    */
    function closeRegisterAdminModel(e) {
        e.preventDefault();
        //close it
        document.getElementById("registerAdminModel").style.display = "none";
    }

    /* Handle opening of a modal
    */
    function openRegisterAdminModel() {
        //close configModal if open
        document.getElementById("configModal").style.display = "none";
        document.getElementById("changePasswordModel").style.display = "none";
        //open registerAdmin form
        document.getElementById("registerAdminModel").style.display = "block";
    }

    /* Handle the closing of a modal
    */
    function closeChangePasswordModel(e) {
        e.preventDefault();
        //close it
        document.getElementById("changePasswordModel").style.display = "none";
    }

    /* Handle opening of a modal
    */
    function openChangePasswordModel() {
        //close registerAdminModel if opening
        document.getElementById("registerAdminModel").style.display = "none";
        document.getElementById("configModal").style.display = "none";
        //open it
        document.getElementById("changePasswordModel").style.display = "block";
    }


    //add the event listeners

    creates = document.getElementsByClassName('createGameButton');
    for (i = 0; i < creates.length; i ++) {
        creates[i].addEventListener("click", createGame)
    }

    document.forms["configUpload"]["upload"].addEventListener("click", handleUpload);

    document.forms["configUpload"]["cancel"].addEventListener("click", closeConfigModal);

    document.getElementById("manageConfigs").addEventListener("click", openConfigModal);

    document.getElementById("registerAdmin").addEventListener("click",openRegisterAdminModel);

    document.forms["registerAdmin"]["cancel"].addEventListener("click", closeRegisterAdminModel);

    document.getElementById("changePassword").addEventListener("click",openChangePasswordModel);

    document.forms["changePassword"]["cancel"].addEventListener("click", closeChangePasswordModel);

    document.getElementById("endGame").addEventListener("click", endGame);

    document.getElementById("logout").addEventListener("click", logout);
}, false);
