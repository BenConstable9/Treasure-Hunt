/*Shows an alert of the given type with the given text*/
function showAlert(type, text) {
    //Checks if success or not
    if (type == "success") {
        var alertBox = document.getElementById('success');
    } else {
        var alertBox = document.getElementById('error');
    }
    //Changes the alert text to the given text
    alertBox.getElementsByTagName('span')[0].innerHTML = text;
    alertBox.style.display = "block";
    setTimeout(function(){
        alertBox.style.display = "none";
    }, 10000);
}

/*Shows the responsive navigation bar*/
function showResponsiveMenu()
{
    var topNav = document.getElementById("myTopnav");
    if (topNav.className === "topnav")
    {
        topNav.className += " responsive";
    }
    else
    {
        topNav.className = "topnav";
    }
}
