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
        console.log(response);
        var table = document.getElementById("configTable");
        table.style.display = "table";

        var row = table.getElementsByTagName('body')[0];

        row.insertCell(0).innerHTML = response.ID;
        row.insertCell(1).innerHTML = response.Name;
        row.insertCell(2).innerHTML = response.FinalLocation;
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

    creates = document.getElementsByClassName('createGameButton');
    for (i = 0; i < creates.length; i ++) {
        creates[i].addEventListener("click", createGame)
    }

    document.forms["configUpload"]["upload"].addEventListener("click", handleUpload);
}, false);
