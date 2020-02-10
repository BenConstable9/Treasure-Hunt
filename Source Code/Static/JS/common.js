function showAlert(type, text) {
    if (type == "success") {
        var alertBox = document.getElementById('success');
    } else {
        var alertBox = document.getElementById('error');
    }
    alertBox.getElementsByTagName('span')[0].innerHTML = text;
    alertBox.style.display = "block";
    setTimeout(function(){
        alertBox.style.display = "none";
    }, 5000);
}