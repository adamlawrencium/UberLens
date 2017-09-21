var PythonShell = require('python-shell');

module.exports = function (lat, lng, walkpref) {
    let pref;
    if (walkpref == 5) {pref = 2}
    else if (walkpref == 10) {pref = 3}
    else if (walkpref == 15) {pref = 4}
    else throw new Error();

    const options = {
        mode: 'json',
        args: [lat, lng, pref, 250] // lat, lng, depth, major
    };

    return new Promise((resolve, reject) => {
        PythonShell.run('hexmath.py', options, function (err, results) {
            if (err) {
                console.log(err);
                reject(err);
            } else {
                resolve(results[0]);
                // console.log(results[0]);
            }
        });
    });
}