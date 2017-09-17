var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var hexGen = require('./routes/hexGen.js');
const axios = require('axios');

var index = require('./routes/index');
var users = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', index);
app.use('/users', users);

app.get('/lens/', async function (req, res) {
  // get origin, destination, walkpref
  // const origin = req.query.origin;
  // const dest = req.query.dest;
  const walkpref = req.query.walkpref;

  // DEV INPUTS
  const msft_seattle = '320 Westlake Ave N, Seattle, WA 98109'
  const msft_studioG = '3950 148th Ave NE, Redmond, WA 98052'
  const studio_D = '15030 NE 36th St, Redmond, WA 98052'
  const center_seattle = '832 16th Ave, Seattle, WA 98122'
  const molly_moons = '917 E Pine St, Seattle, WA 98122'
  const msft_bellevue = '205 108th Ave NE, Bellevue, WA 98004'
  const msft_redmond = '15010 Northeast 36th Street, Redmond, WA 98052'
  const larkspur = '15805 SE 37th St, Bellevue, WA 98006'

  // FEED INPUTS TO GOOGLE MAPS API FOR GEOCODING AIzaSyC6PgCIuxWBNY3ITEakn8lxczgAqzzIgps
  // origin address to lat, lng
  // destination address to lat, lng 

  // Create client with a Promise constructor
  const googleMapsClient = require('@google/maps').createClient({
    key: 'AIzaSyC6PgCIuxWBNY3ITEakn8lxczgAqzzIgps', // this will be replaced...
    Promise: Promise // 'Promise' is the native constructor.
  });

  // Geocode an origin and destination
  let orig = await googleMapsClient.geocode({ address: studio_D }).asPromise();
  // console.log(orig.json.results[0].geometry.location);
  let dest = await googleMapsClient.geocode({ address: molly_moons }).asPromise();
  // console.log(dest.json.results);
  // console.log();

  let r = await googleMapsClient.reverseGeocode({ place_id: 'ChIJWZYFhG1tkFQRHqN9zKkOIS0' }).asPromise();
  // console.log(r.json.results);

  // GENERATE HEX GRID (inputs: destination latlng)
  const orig_lat = orig.json.results[0].geometry.location.lat;
  const orig_lng = orig.json.results[0].geometry.location.lng;
  let hexGrid;
  try {
    hexGrid = await hexGen(orig_lat, orig_lng);
    // console.log(hexGrid)
  } catch (error) {
    res.json(error);
  }

  // FILTER OUT LAT,LNG IN WATER
  let testForWater = hexGrid.map((loc, index) => { return { lat: loc[0], lng: loc[1] } });
  testForWater = await googleMapsClient.elevation({ locations: testForWater }).asPromise();
  let notWater = testForWater.json.results.filter(location => { return location.elevation > 5 });
  hexGrid = notWater.map(loc => { return { lat: loc.location.lat, lng: loc.location.lng } });

  // TURN LAT LNGS INTO GOOGLE PLACE IDS
  let placeID_Queries = hexGrid.map(loc => {
    return googleMapsClient.reverseGeocode({ latlng: [loc.lat, loc.lng] }).asPromise();
  });
  let reverseGeocodeRes = await Promise.all(placeID_Queries);
  let placeIDs = reverseGeocodeRes.map(entry => { return entry.json.results[0].place_id; });
  // console.log(placeIDs);

  // CALL UBER API ON ALL PLACE IDS
  let uberReqURL = 'https://www.uber.com/api/fare-estimate?pickupRef=' + placeIDs[0] + '&destinationRef=';
  // let uberFares = placeIDs.map( id => { await axios.get(uberReqURL + id)})
  let uberFareReqs = [];
  for (let i = 1; i < placeIDs.length; i++) {
    uberFareReqs.push(axios.get(uberReqURL + placeIDs[i]));
  }

  // Parse Uber response
  uberFareRes = await Promise.all(uberFareReqs);
  let uberFares = []
  for (let i = 0; i < uberFareRes.length; i++) {
    uberFares.push(uberFareRes[i].data);
  }

  // Get only UberX
  uberFares = uberFares.map(fareData => {
    for (let i = 0; i < fareData.prices.length; i++) {
      if (fareData.prices[i].vehicleViewDisplayName == 'uberX') {
        console.log('hola');
        return fareData.prices[i];
      }
    }
  });
  console.log(uberFares);
  // let minFare = 99999;
  // for (let i = 0; i < uberFares)

  // CREATE MASTER FARE OBJECT WITH LAT,LNG's
  // let latlng_fareObj = hexGrid.map( (point, index) => {})
  // uberFares = uberFares.map(res => console.log(res.res));
  res.json(uberFares)



});


// catch 404 and forward to error handler
app.use(function (req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
