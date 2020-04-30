const $map = document.querySelector('#map')
const $autocomplete = document.querySelector('#autocomplete')
const $errorMessage = document.querySelector('#error-message')
const $address = document.querySelector('#address')
const $latitude = document.querySelector('#latitude')
const $longitude = document.querySelector('#longitude')

let autocomplete, map, marker, geocoder, infowindow;

function startLocationServices() {
  autocomplete = new google.maps.places.Autocomplete($autocomplete, {types: ['geocode']});
  autocomplete.setFields(['geometry']);
  autocomplete.addListener('place_changed', getLocation);
  
  map = new google.maps.Map($map, {
    center: {lat: 19.432608, lng: -99.133209}, // Mexico City
    zoom: 10,
    streetViewControl: false,
  });
  map.addListener('click', function(e) {
    placeMarker(e.latLng);
  });

  geocoder = new google.maps.Geocoder();
  infowindow = new google.maps.InfoWindow({
    size: new google.maps.Size(150, 50)
  });
}

function geocodePosition(location) {
  infowindow.close();
  geocoder.geocode({
    latLng: location
  }, function(responses) {
    if (responses && responses.length > 0) {
      marker.formatted_address = responses[0].formatted_address;
    } else {
      marker.formatted_address = null;
    }
    infowindow.setContent(marker.formatted_address ? marker.formatted_address : 'No se puede determinar la dirección en está ubicación.');
    infowindow.open(map, marker);
    $address.value = $autocomplete.value = marker.formatted_address
    latitude.value = location.lat()
    longitude.value = location.lng()
  });
}

function placeMarker(position) {
  if (!marker) {
    marker = new google.maps.Marker({
      position: position,
      map: map
    });
    map.panTo(position);
  } else {
    marker.setPosition(position)
  }
  map.setZoom(17);
  geocodePosition(position)
}

function getLocation() {
  if ($autocomplete.classList.contains('is-invalid')) {
    $autocomplete.classList.remove('is-invalid')
    $errorMessage.style.display = 'none';
  }
  const place = autocomplete.getPlace();

  if (place.geometry) {
    const location = place.geometry.location
    placeMarker(location)
  }

}

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      const geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      const circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}


$autocomplete.addEventListener('change', () => {
  if (!$autocomplete.value) {
    $address.value = ""
    $latitude.value = ""
    $longitude.value = ""
    map.setZoom(10)
    map.panTo({lat: 19.432608, lng: -99.133209}); // Mexico
    infowindow.close();
  }
})