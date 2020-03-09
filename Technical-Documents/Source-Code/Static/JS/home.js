/* Author - Ben Constable
   Modified By - Ravi Gohel
   Handle the ajax functions for creating and uploading games
*/

document.addEventListener('DOMContentLoaded', function(){


    //Function that fills the select input with the tutors associated with the subject based on the gamePin the team entered
    function handleSection(response){
        var options = document.getElementById("tutorsNames");
        if (response.tutorNames){ //If the gamePin is valid
            for(var i = 0; i < response.tutorNames.length; i++) {
                var tutor = response.tutorNames[i];
                var option = document.createElement("option"); //creates option
                option.textContent = tutor; //what the user sees
                option.value = response.tutorIDs[i]; //the value which is associated with the option
                options.appendChild(option); //adds the new option to bottom of the select
            }
        }
        else {
            var options = document.getElementById("tutorsNames");
            document.getElementById("tutorsNames").innerHTML = "";
            var option = document.createElement("option"); //creates option
            //gives it the properties of an "empty" non selectable dropdown option
            option.value = "";
            option.disabled = true;
            option.selected = true;
            option.textContent = "Select"
            options.appendChild(option);
        }
    }

    //Function that obtains the pin value and calls for its verification
    function gameFunction(){
        var pin = document.getElementById("GamePin").value;

        HTTPGet("/verifyPin?GamePin=" + pin, handleSection)
    }

    //GamePin listener for when the entered game pin changes
    document.getElementById("GamePin").addEventListener("input", gameFunction);
}, false);
