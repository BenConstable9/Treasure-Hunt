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

//This function appends the responsive class to topNav on click of the mobile menu. This creates the responsive stacked menu
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
