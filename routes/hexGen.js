var PythonShell = require('python-shell');

// let lat = 47.641387;
// let lng = -122.132817;
// let depth = 3;
// let major = 200;


module.exports = function (lat, lng) {

    const options = {
        mode: 'json',
        args: [lat, lng, 6, 200] // lat, lng, depth, major
    };

    return new Promise((resolve, reject) => {
        PythonShell.run('hexmath.py', options, function (err, results) {
            if (err) {
                console.log(err)
                reject(err);
            } else {
                resolve(results[0]);
                // console.log(results[0]);
            }
        });
    });
}