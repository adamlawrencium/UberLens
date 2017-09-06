<p align="center">
    <img src="https://user-images.githubusercontent.com/10917080/30120320-7c6aa6b4-92f6-11e7-9949-5479fa241969.png" width=600/>
</p>


# UberLens - visualize Uber fare rates in your area
From an origin to a destination:
![blah](https://raw.githubusercontent.com/adamalawrence/UberLens/master/Screen%20Shot%202017-06-29%20at%2012.46.16%20AM.png)
Fares surrounding a certain location (first attempt at visualizing fares:
![hmm check the repo for the pic](https://raw.githubusercontent.com/adamalawrence/UberLens/master/Screen%20Shot%202017-06-27%20at%2012.39.10%20AM.png)


### Notes
*Get data --> visualize data*

Microsoft office locations:
- Redmond
- Bellevue
- Seattle

From each office, we want to visualize how Uber's fares change within a certain radius. Perhaps we'll see price spikes at points of interest (POIs)... Perhaps we'll see a nice gradient... It'd also be interesting to see how the fares change over time, if they change at all.

That said, here's the flow of information: Coordinate points of addresses -> Get fare estimate from origin to address -> visualize fares on a map. Here's our data sources:

- Addresses - From list of coordinates, remove those that don't correspond to a valid address.
- From origin to every lat lng pair, call Uber API to get a fare estimate.

Plot [lat, lng, fare] on a map.

Pretty straightforward!
