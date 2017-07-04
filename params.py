import math
# defaultmode = 'walking'
defaultmode = 'driving'
albany_washingtonpark = [42.66,-73.77]#(mapsize/2,mapsize/2)
tvcog = [42.731125,-73.6902487]
manhattan = [40.7831,-73.9712]
bellevue = [47.6124808, -122.1969143]
seattle = [47.610117, -122.310822]
studioG = [47.645099, -122.141035]
building_44 = [47.641387,-122.132817]
rpi = [42.73,-73.68]
schdy = [42.81,-73.94]
centroid = building_44
LTM = True
pilImage = False
major = 80
mapsize = 600
scaletime = 3600 # seconds, maximum travel time for scaling
shells = 5

edgelen = major
#fudge factor for longitude shrink, rounding. Experimentally determined
latfud = 0.9985/math.cos(math.radians(centroid[0]))
lonfud = 0.9981
opacity = 0.5
strokeWeight=0
#centroid = (mapsize/2,mapsize/2)
templateFile = 'shapesbase.html'
heatmapTemplateFile = 'templates/heatmap_template.html'
heatmapOutputFile = 'webout/heatmap.html'
baseName = '{}_{}_{}_{}'.format(centroid[0],centroid[1], shells, major).replace('.', '_')
coordFile = 'data/{}'.format(baseName)
trackingFile = 'data/tr_{}'.format(baseName)
elementsFile = 'data/el_{}'.format(baseName)
outputFile = 'webout/{}__hexoverlay.html'.format(baseName)

# Request parameters
autoCycles = 1
