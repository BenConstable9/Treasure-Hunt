var map;

function createMap() {
  var uni = {lat: 50.737, lng: -3.535};
  var har = {lat: 50.737969, lng: -3.532290};
  var options = {
    zoom: 16,
    center: uni
  };
  map = new google.maps.Map(document.getElementById('map'), options);
  var marker = new google.maps.Marker({position: har, map: map});
}
