function HTTPPost(url, params, callback) {
    //perform a HTTP post Request
    //param url: the url to send the request to
    //param params: The http post params to Send
    //param callback: the function to send the response to

    //open a new request
    var request = new XMLHttpRequest();

    //handle the async completing
    request.onreadystatechange = function() {
    	if(request.readyState == 4 && request.status == 200) {
            //pass the response to the callback
    		callback(request.response);
    	}
    }

    //open the request and set the response type
    request.open("POST", url, true);
    request.responseType = "json";

    //Send the proper header information along with the request
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(params);
}

function HTTPUploadFile(url, data, callback) {
    //perform a HTTP post Request
    //param url: the url to send the request to
    //param params: The http post params to Send
    //param callback: the function to send the response to

    //open a new request
    var request = new XMLHttpRequest();

    //handle the async completing
    request.onreadystatechange = function() {
    	if(request.readyState == 4 && request.status == 200) {
            //pass the response to the callback
    		callback(request.response);
    	}
    }

    //open the request and set the response type
    request.open("POST", url, true);
    request.responseType = "json";

    //Send the proper header information along with the request
    request.send(data);
}

function HTTPGet(url, callback) {
    //perform a HTTP get Request
    //param url: the url to send the request to
    //param callback: the function to send the response to

    //open a new request
    var request = new XMLHttpRequest();

    request.onreadystatechange = function() {
        // state 4 is when the request is complete
        if (request.status == 200 && request.readyState == 4) {
            //pass te response to the callback
            callback(request.response);
        }
    }

    //make the request, set as JSON as we know it will be
    request.open("GET", url, true);
    request.responseType = "json";
    request.send();
}
