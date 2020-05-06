const $map = document.querySelector('#map')

let map;

function startLocationServices() { 
  const location = {lat: latitude, lng: longitude}

  map = new google.maps.Map($map, {
    center: location, 
    zoom: 17,
    streetViewControl: false,
  });

  placeMarker(location);
}

function placeMarker(position) {
  marker = new google.maps.Marker({
    position: position,
    map: map
  });
  map.panTo(position);
}

