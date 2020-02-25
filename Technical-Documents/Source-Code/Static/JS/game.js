document.addEventListener('DOMContentLoaded', function(){

    function createGameCallback(response) {
        if (response.status == "1") {
            document.getElementById('gamePin').value = "Current Game Pin: " + response.GamePin;
            creates = document.getElementsByClassName('createGameButton');
            for (i = 0; i < creates.length; i ++) {
                creates[i].disabled = true;
            }
            showAlert("success", "Game started successfully!");
            document.getElementById("endGame").disabled = false;
            document.getElementById("endGame").innerHTML = "End Game";
        }
    }

    function createGame() {
        subjectID = JSON.parse(this.dataset.json.replace(/'/g, '"')).SubjectID;
        var params = "SubjectID=" + subjectID;
        HTTPPost("/admin/game/create", params, createGameCallback)
    }

    function handleUploadCallback(response) {
        if (document.getElementById('noConfigError')) {
            document.getElementById('noConfigError').style.display = "none";
        }
        var table = document.getElementById("configTable");
        table.style.display = "table";

        var row = table.getElementsByTagName('tbody')[0].insertRow(0);

        buttonJSON = JSON.stringify(response);

        row.insertCell(0).innerHTML = response.SubjectID;
        row.insertCell(1).innerHTML = response.SubjectName;
        row.insertCell(2).innerHTML = response.Building;
        row.insertCell(3).innerHTML = '<button id="create' + response.SubjectID + '" class="createGameButton">Create Game</button>';
        row.insertCell(4).innerHTML = '<button id="print' + response.SubjectID + '" class="printQRCode">Print QR Codes</button>';

        document.getElementById('create' + response.SubjectID).addEventListener("click", createGame);
        document.getElementById('create' + response.SubjectID).dataset.json = buttonJSON;
        //todo add the event listener for the response
    }

    function handleUpload(e) {
        e.preventDefault();
        var form = document.forms["configUpload"];
        console.log(form["file"])
        var formData = new FormData();
        console.log(form["file"].files)
        formData.append("file", form["file"].files[0]);
        console.log(formData)

        HTTPUploadFile("/admin/upload", formData, handleUploadCallback);
    }

    function closeConfigModal(e) {
        e.preventDefault();
        document.getElementById("configModal").style.display = "none";
    }

    function openConfigModal() {
        document.getElementById("configModal").style.display = "block";
    }

    creates = document.getElementsByClassName('createGameButton');
    for (i = 0; i < creates.length; i ++) {
        creates[i].addEventListener("click", createGame)
    }

    document.forms["configUpload"]["upload"].addEventListener("click", handleUpload);

    document.forms["configUpload"]["cancel"].addEventListener("click", closeConfigModal);

    document.getElementById("manageConfigs").addEventListener("click", openConfigModal);
}, false);
