// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBIwzALxUPNbatRBj3Xi1Uhp0fFzwWNBkE&libraries=places">
let map;
let service;
let infowindow;
let sydney;
let rad;
let mapZoom;
let startLocation;

function initMap() {
  
  sydney = new google.maps.LatLng(-33.8665433,151.1956316);
  infowindow = new google.maps.InfoWindow();
  rad = 5000;
  map = new google.maps.Map(document.getElementById("map"), {
    center: sydney,
    zoom: 1
  });
  search("publisher");
  

/*google.maps.event.addListener(map, 'click', function(event) {
    mapZoom = map.getZoom();
    startLocation = event.latLng;
    setTimeout(placeMarker, 600);
});
*/

/*
initialize();*/
}

//crawlMap('', rad, lat, long)
function crawlMap(q, rad_, lat, long) {

  sydney = new google.maps.LatLng(lat, long);
  infowindow = new google.maps.InfoWindow();
  rad = rad_;
document.addEventListener("click", onc);
  search(q);
/*
initialize();*/
}
function search(q){
resx = [];
const request = {
    //query: '"'+q+'"',
    location: sydney,
    radius:rad,
    types:["electronics_store", "hardware_store", "book_store", "store"]
  };
  service = new google.maps.places.PlacesService(map);
  service.nearbySearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      for (let i = 0; i < results.length; i++) {
        if(false){continue;}//results[i].user_ratings_total<0
        createMarker(results[i]);
        //console.log(results[i].name,results[i].place_id);
        resx.push(results[i].place_id);
        try {
  //console.log(results[i].name, results[i].formatted_phone_number);
}
catch(err) {
  console.log("error");
}
        
      }
      map.setCenter(results[0].geometry.location);
    }

for(let o = 0;o<resx.length;o++){
 console.log(getDetails_(resx[o]));
}
    console.log({'status':status, 'results':results});
  });
}
function createMarker(place) {
  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
  });
  google.maps.event.addListener(marker, "click", () => {
    infowindow.setContent(place.name);
    infowindow.open(map);
  });
}
function onc(){
crawlMap('q', 5000,map.getCenter().lat(),map.getCenter().lng());
}
function initialize() {
  var pyrmont = new google.maps.LatLng(-33.8665433,151.1956316);

  map = new google.maps.Map(document.getElementById('map'), {
      center: pyrmont,
      zoom: 15
    });

  var request = {
    
    query: "publishers",
    fields: ["name", "geometry"],
    radius:500
};

  service = new google.maps.places.PlacesService(map);
  service.nearbySearch(request, callback);
}

function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      createMarker(results[i]);
    }
  }
}
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, true ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
function getDetails_(pid){
const request_ = {
    placeId: pid,
    fields: ["name", "formatted_address", "place_id", "geometry", "website"],
  };
  infowindow = new google.maps.InfoWindow();
  service = new google.maps.places.PlacesService(map);
  service.getDetails(request_, (place, status) => {
    try{
    if(place.website == undefined)
    {
    }
else{
console.log(place.name, place.website);
httpGet('http://localhost:5003/new_reseller?website='+place.website+'&bname='+place.name+'&country='+'your country'+'&lat='+place.geometry.location.lat()+'&long='+place.geometry.location.lng())
}
}
    catch(er){
	return;
	}
     if (status === google.maps.places.PlacesServiceStatus.OK) {
      const marker = new google.maps.Marker({
        map,
        position: place.geometry.location,
      });
      google.maps.event.addListener(marker, "click", function () {
        infowindow.setContent(
          "<div><strong>" +
            place.name +
            "</strong><br>" +
            "Lat/Lon: <br>" +
            place.geometry.location.lat()+"<t/>/<t/>"+place.geometry.location.lng() +
            "<br>Website: " +
            place.website +
            "<br>" +
            pid.user_ratings_total +
            "</div>"
        );
        infowindow.open(map, this);
        
        
      });
    }
  });
}
        
/**/
