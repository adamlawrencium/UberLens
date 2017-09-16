var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var hexGen = require('./routes/hexGen.js');

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
  const origin = req.query.origin;
  const dest = req.query.dest;
  const walkpref = req.query.walkpref;

  // let lat = 47.641387;
  // let lng = -122.132817;
  // let depth = 3;
  // let major = 10;
  // var options = {
  //   mode: 'json',
  //   args: [lat, lng, depth, major]
  // };
  try {
    let data = await hexGen();
    console.log(data);
    res.json(data);
  } catch (error) {
    // res.json(error);
  }

  // .then( data => {
  //   res.json(data);
  // })
  // .catch( err => {
  //   res.json
  // })
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
