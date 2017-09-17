
const building_44 = [47.641387,-122.132817];
const centroid = building_44;
const latfud = 0.9985/Math.cos( centroid[0] * (Math.PI / 180))
const lonfud = 0.9981
const SIN60 = Math.sin( (Math.PI / 180) * 60 )

function getHexNeighbors(x, y, major, ltm) {
    if (ltm) {
        major /= 111120
    }
    var aa = 1.5 * major * lonfud
    var cc = major * SIN60 * latfud
    var lst = [[x, y + 2 * cc], [x + aa, y + cc], [x + aa, y - cc], [x - aa, y - cc], [x, y - 2 * cc], [x - aa, y + cc]];
    return lst;
}

function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}
function latlonHash(x,y, prec) {
    x_ = Math.abs(round(x, 6));
    y_ = Math.abs(round(y, 6));
    return x_.toString() + y_.toString();
}


function generateHexgrid(x, y, depth, major) {
    let hexCenters = [[x,y]];
    let hexHashes = [latlonHash(x, y)];
    console.log(hexHashes);
    lastShellSize = 0;

    // Loop through main layers
    for (let i = 2; i < depth + 1; i++) {
        let active = [hexCenters[-lastShellSize]];

        // Loop through outermost layer
        for (let j = 0; j < active.length; j++) {
            console.log(active);
            let newNodes = getHexNeighbors(active[j][0], active[j][1], 14);            
            // console.log(newNodes);
            // process.exit(0);
            // Loop through outmost nodes' neighbors
            for (let k = 0; k < newNodes.length; k++) {
                llhash = latlonHash(newNodes[k]);
                // console.log(llhash,hexHashes);
                    // console.log(hexHashes.indexOf(llhash));
                if (hexHashes.indexOf(llhash) !== -1) {
                    hexCenters.push(newNodes[k]);
                    hexHashes.push(llhash);
                }
            }
        }
        lastShellSize += 6;
    }
    // console.log(hexCenters);
}

// getHexNeighbors(47.641387, -122.132817, 1, true);
// generateHexgrid(47.641387, -122.132817, 3, 10);