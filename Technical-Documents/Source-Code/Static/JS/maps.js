var map;
var response;
var uni = {lat: 50.737, lng: -3.535};
var har = {lat: 50.737969, lng: -3.532290};
var options = {
  zoom: 16,
  center: uni
};
function createMap() {

  map = new google.maps.Map(document.getElementById('map'), options);
  HTTPGet("/getPins", handleSection)
}

function handleSection(res){
  response = res.data;
  for (var i = 0; i < response.length; i++) {
    var row = response[i];
    var place = {lng:parseFloat(row.latitude), lat: parseFloat(row.longitude)}
    var marker = new google.maps.Marker({position: place, map: map});
  }
}
