/* Author - Ben Constable
   Handle the dashboard functionality
*/

document.addEventListener('DOMContentLoaded', function(){
    let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
    scanner.addListener('scan', function (content) {
        verifyLocation(content);
    });
    Instascan.Camera.getCameras().then(function (cameras) {
        if (cameras.length > 0) {
            scanner.start(cameras[0]);
        } else {
            showAlert("error", "No Camera Installed");
        }
    }).catch(function (e) {
        showAlert("error", e);
    });

    function verifyLocationCallback(response) {
        console.log(response);
    }

    /* Fetch the question for the given QR Code */
    function verifyLocation(value) {
        //send off our request
        HTTPPost("/dashboard/verifylocation", "value=" + value, verifyLocationCallback)
    }

    /*toggles bettween displaying and hiding the scan model*/
    function flipScanModel(e){

        if (document.getElementById("scanModal").style.display === "block"){
          document.getElementById("scanModal").style.display = "none";
        }else{
          document.getElementById("scanModal").style.display = "block"
        }
    }

    document.getElementById("flipScanModel").addEventListener("click", flipScanModel);
});
