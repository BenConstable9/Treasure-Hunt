/* Author - Ben Constable
   Modified - Ravi Gohel
   Handle the ajax functions for creating and uploading games
*/

document.addEventListener('DOMContentLoaded', function(){

  /* Handle the response from changing admin password */
    function changePasswordCallback(response) {
        if (response.status == "0") {
            //incorrect response
            showAlert("changePasswordModalError", "Error in Changing Password - not the same");
        } else {
            //Tell user password has been changed
            showAlert("success", "Password change successfully");
            var passwordForm = document.forms["changePassword"];
            passwordForm.reset();
            document.getElementById("changePasswordModal").style.display = "none";
          }
    }

  /* Handles the changing of admin password */
    function changePassword(e){
      e.preventDefault();
      //validate the password
      var password1 = document.forms["changePassword"]["password1"].value;
      var password2 = document.forms["changePassword"]["password2"].value;
      var id = document.forms["changePassword"]["ID"].value;
      if (password1 == password2 && password1.length >= 1){
        //send off the request
        HTTPPost("/admin/game/changePassword", "password1=" + password1 + "&password2=" + password2 + "&ID=" + id, changePasswordCallback)
      }
      else if (password1.length ==0 || password2.length ==0){
        showAlert("changePasswordModalError", "Error in Changing Password - Empty Password Input")
      }
      else{
        showAlert("changePasswordModalError", "Error in Changing Password - Not The Same");
      }
    }

  /* Handle the response from registering new admin */
    function registerAdminCallback(response) {
      if (response.status == "1") {
          //Tell the user the admin has been added
          showAlert("success", "New admin registered successfully")
          var registerForm = document.forms["registerAdmin"]
          registerForm.reset();
          document.getElementById("registerAdminModal").style.display = "none";
      }
      else {
        showAlert("adminRegisterModalError", "Error in registering");
        }
    }

  /* Handle the registering of a new admin */
    function registerAdmin(e){
      e.preventDefault();
      //validate the password
      var name = document.forms["registerAdmin"]["name"].value;
      var username = document.forms["registerAdmin"]["username"].value;
      var password1 = document.forms["registerAdmin"]["password1"].value;
      var password2 = document.forms["registerAdmin"]["password2"].value;
      if (password1 == password2 && password1.length >= 1 && name.length >= 1 && username.length >= 1 && /^[a-zA-Z]+$/.test(name) == true){
        //send off the request
        HTTPPost("/admin/game/register", "password1=" + password1 + "&password2=" + password2 + "&name=" + name + "&username=" + username, registerAdminCallback)
      }
      else{
        showAlert("registerAdminModalError", "Error in your registration");
      }
    }


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
        document.getElementById("loadingContainer").style.display = "none";
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
            row.insertCell(5).innerHTML = '<button id="delete' + response.SubjectID + '" class="deleteSubjectButton">Delete Subject</button>';

            //add the event listeners
            document.getElementById('create' + response.SubjectID).addEventListener("click", createGame);
            document.getElementById('create' + response.SubjectID).dataset.json = buttonJSON;
            document.getElementById('print' + response.SubjectID).addEventListener("click", createPrints);
            document.getElementById('print' + response.SubjectID).dataset.json = buttonJSON;
            document.getElementById('delete' + response.SubjectID).addEventListener("click", deleteSubject);
            document.getElementById('delete' + response.SubjectID).dataset.json = buttonJSON;
        } else {
            showAlert("error", response.message);
        }
    }

  /* Handle the submission of the game form
    */
    function handleUpload(e) {
        //stop a page reload
        e.preventDefault();

        document.getElementById("loadingContainer").style.display = "block";

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
        //close registerAdminModal if opening
        document.getElementById("registerAdminModal").style.display = "none";
        document.getElementById("changePasswordModal").style.display = "none";
        //open it
        document.getElementById("configModal").style.display = "block";
    }

    /* Handle the closing of a modal
    */
    function closeRegisterAdminModal(e) {
        e.preventDefault();
        var registerForm = document.forms["registerAdmin"];
        registerForm.reset();
        //close it
        document.getElementById("registerAdminModal").style.display = "none";
    }

    /* Handle opening of a modal
    */
    function openRegisterAdminModal() {
        //close configModal if open
        document.getElementById("configModal").style.display = "none";
        document.getElementById("changePasswordModal").style.display = "none";
        //open registerAdmin form
        document.getElementById("registerAdminModal").style.display = "block";
    }

    /* Handle the closing of a modal
    */
    function closeChangePasswordModal(e) {
        e.preventDefault();
        var passwordForm = document.forms["changePassword"]
        passwordForm.reset();
        //close it
        document.getElementById("changePasswordModal").style.display = "none";
    }

    /* Handle the closing of a modal
    */
    function closeQuestionsModal(e) {
        e.preventDefault();
        //close it
        document.getElementById("questionsModal").style.display = "none";
    }

    /* Handle opening of a modal
    */
    function openChangePasswordModal() {
        //close registerAdminModal if opening
        document.getElementById("registerAdminModal").style.display = "none";
        document.getElementById("configModal").style.display = "none";
        //open it
        document.getElementById("changePasswordModal").style.display = "block";
    }

    /* Handle submission of clicking print QR codes
    */
    function createPrints(){
        subjectID = JSON.parse(this.dataset.json.replace(/'/g, '"')).SubjectID;
        HTTPGet("/admin/questions?subject=" + subjectID, createPrintsCallback);

    }

    /* Handles displaying the QR codes
    */
    function createPrintsCallback(response){
        if (response.status == "0") {
            showAlert("error", response.message);
        } else {
            document.getElementById("questionsModalList").innerHTML = '';
            //Loops through data from questions and adds a link to QR code for each location
            for (i = 0; i < response.data.length; i ++) {
                var x = document.createElement("LI");
                x.innerHTML = "<a href='/Static/Images/Codes/" + response.data[i].questionID + ".svg' target='_blank'>" + response.data[i].building + "</a>";
                document.getElementById("questionsModalList").appendChild(x);
            }
            //Closes modals
            document.getElementById("configModal").style.display = "none";
            document.getElementById("questionsModal").style.display = "block";
        }
    }

    /* Handle the callback getting the notifications

        :param response: The response from the request
    */
    function fetchNotificationsCallback(response) {
        document.getElementById("notificationsList").innerHTML = "";
        if (response.status == "0" && response.message != "No Game Running") {
            //set the error as this
            showAlert("error", response.message);
            document.getElementById("notificationsError").style.display = "block";
        } else if (response.status == "1" && response.data.length > 0) {
            //output the notifications
            document.getElementById("notificationsError").style.display = "none";
            //Add all the teams to the lists
            for (i = 0; i < response.data.length; i ++) {
                //put the data in
                var x = document.createElement("LI");
                x.innerHTML = "<span class='teamName'>" + response.data[i].TeamName + "</span> " + response.data[i].Action + " <span class='teamName'> @ " + response.data[i].Time.split(" ")[1].substring(0,5) + "</span>";
                document.getElementById("notificationsList").appendChild(x);
            }
        } else {
            //no game running
            document.getElementById("notificationsError").style.display = "block";
        }
    }

    /* Fetch Notifications */
    function fetchNotifications() {
        HTTPGet("/admin/notifications", fetchNotificationsCallback);
    }

    /* Send off a request to delete a subject
    */
    function deleteSubject(){
        //Get the subject ID to pass to the request
        subjectID = JSON.parse(this.dataset.json.replace(/'/g, '"')).SubjectID;
        document.getElementById("loadingContainer").style.display = "block";
        var params = "SubjectID=" + subjectID;
        HTTPPost("/admin/deleteSubject", params, deleteSubjectCallback)
    }

    /* Handle the callback from ending a game

        :param response: The response from the request
    */
    function deleteSubjectCallback(response) {
        if (response.status == "1") {
            document.getElementById("loadingContainer").style.display = "none";
            //Delete subject row from table
            document.getElementById("configTable").deleteRow(1);
            document.getElementById('noConfigError').style.display = "block";
            //show message
            showAlert("success", response.message);
            document.reload();
        } else {
            showAlert("error", response.message);
        }
    }

    //add the event listeners

    creates = document.getElementsByClassName('createGameButton');
    for (i = 0; i < creates.length; i ++) {
        creates[i].addEventListener("click", createGame)
    }

    prints = document.getElementsByClassName('printQRCode');
    for (i = 0; i < prints.length; i ++) {
        prints[i].addEventListener("click", createPrints)
    }

    deletes = document.getElementsByClassName('deleteSubjectButton');
    for (i = 0; i < deletes.length; i ++) {
        deletes[i].addEventListener("click", deleteSubject)
    }

    document.forms["configUpload"]["upload"].addEventListener("click", handleUpload);

    document.forms["configUpload"]["cancel"].addEventListener("click", closeConfigModal);

    document.getElementById("manageConfigs").addEventListener("click", openConfigModal);

    document.getElementById("registerAdmin").addEventListener("click",openRegisterAdminModal);

    document.forms["registerAdmin"]["cancel"].addEventListener("click", closeRegisterAdminModal);

    document.forms["registerAdmin"]["signUp"].addEventListener("click",registerAdmin);

    document.getElementById("changePassword").addEventListener("click",openChangePasswordModal);

    document.forms["changePassword"]["cancel"].addEventListener("click", closeChangePasswordModal);

    document.forms["changePassword"]["submit"].addEventListener("click",changePassword);

    document.getElementById("endGame").addEventListener("click", endGame);

    document.getElementById("logout").addEventListener("click", logout);

    document.getElementById("cancelQuestionsModal").addEventListener("click", closeQuestionsModal);

    //document.getElementsByClassName('deleteSubjectButton').addEventListener("click", deleteSubject);

    setInterval(function(){ fetchNotifications(); }, 5000);

    fetchNotifications();
}, false);
