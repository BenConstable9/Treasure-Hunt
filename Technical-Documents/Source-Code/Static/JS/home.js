/* Author - Ben Constable
   Modified - Ravi Gohel
   Handle the ajax functions for creating and uploading games
*/

document.addEventListener('DOMContentLoaded', function(){
    function handleSection(response){
        var options = document.getElementById("tutorsNames");
        if (response.tutorNames){
            for(var i = 0; i < response.tutorNames.length; i++) {
                var tutor = response.tutorNames[i];
                var option = document.createElement("option"); //creates html option
                option.textContent = tutor; //what the user sees
                option.value = response.tutorIDs[i]; //the value which is associated with the option
                options.appendChild(option); //adds the new option to bottom of the select
            }
        }
        else {
            var options = document.getElementById("tutorsNames");
            document.getElementById("tutorsNames").innerHTML = "";
            var option = document.createElement("option"); //creates html option
            //gives it the properties of an "empty" non selectable dropdown option
            option.value = "";
            option.disabled = true;
            option.selected = true;
            option.textContent = "Select"
            options.appendChild(option);
        }
    }

    function gameFunction(){
        var pin = document.getElementById("GamePin").value;

        HTTPGet("/verifyPin?GamePin=" + pin, handleSection)
    }

    document.getElementById("GamePin").addEventListener("input", gameFunction);
}, false);
  