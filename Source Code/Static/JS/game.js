document.addEventListener('DOMContentLoaded', function(){

    function createGameCallback(response) {
        console.log(response)
        if (response.status == "1") {
            document.getElementById('GamePin').value = response.GamePin;
        }
    }

    function createGame() {
        subjectID = JSON.parse(this.dataset.json.replace(/'/g, '"')).SubjectID;
        var params = "SubjectID=" + subjectID;
        HTTPPost("/admin/game/create", params, createGameCallback)
    }

    function handleUploadCallback(response) {
        console.log(response);
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
