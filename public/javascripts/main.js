// This example displays an address form, using the autocompleteorigin feature
// of the Google Places API to help users fill in the information.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

var placeSearch, autocompleteorigin, autocompletedestination;
var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    country: 'long_name',
    postal_code: 'short_name'
};

function initAutocomplete() {
    // Create the autocompleteorigin object, restricting the search to geographical
    // location types.
    autocompleteorigin = new google.maps.places.Autocomplete(
            /** @type {!HTMLInputElement} */(document.getElementById('autocompleteorigin')),
        { types: [] });
    autocompletedestination = new google.maps.places.Autocomplete(
            /** @type {!HTMLInputElement} */(document.getElementById('autocompletedestination')),
        { types: [] });

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    // autocompleteorigin.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
    // Get the placeorigin details from the autocompleteorigin object.
    var placeorigin = autocompleteorigin.getPlace();

    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;
    }

    // Get each component of the address from the placeorigin details
    // and fill the corresponding field on the form.
    for (var i = 0; i < placeorigin.address_components.length; i++) {
        var addressType = placeorigin.address_components[i].types[0];
        if (componentForm[addressType]) {
            var val = placeorigin.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val;
        }
    }

    ///////////

    var placedestination = autocompleteorigin.getPlace();

    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;
    }

    // Get each component of the address from the placedestination details
    // and fill the corresponding field on the form.
    for (var i = 0; i < placedestination.address_components.length; i++) {
        var addressType = placedestination.address_components[i].types[0];
        if (componentForm[addressType]) {
            var val = placedestination.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val;
        }
    }
}

// Bias the autocompleteorigin object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            var circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy
            });
            autocompleteorigin.setBounds(circle.getBounds());
            autocompletedestination.setBounds(circle.getBounds());
        });
    }
}

$(document).ready(function () {
    $('#mySpinner').removeClass('spinner');
    google.maps.event.addDomListener(window, 'load', initAutocomplete);
    $('#submitbutton').click(() => {
        $('#mySpinner').addClass('spinner');
        const orig = $('#autocompleteorigin').val();
        const dest = $('#autocompletedestination').val();
        $.getJSON(`/lens?orig=${orig}&dest=${dest}`, (data) => {
            $('#mySpinner').removeClass('spinner');
            console.log(data);
            const minAddr = data['lowestFare'][0]
            const minFare = data['lowestFare'][1]
            $(".jumbotron").append( `<p2>Found a cheaper destination!:</p2> <p>For $${minFare}, ${minAddr}</p>` );
        })
    })


    // $('.btn').on('click', function () {
    //     var $this = $(this);
    //     $this.button('loading');
    //     setTimeout(function () {
    //         $this.button('reset');
    //     }, 8000);
    // });


})