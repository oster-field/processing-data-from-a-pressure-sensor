# processing-data-from-a-pressure-sensor
Processing data from a pressure sensor located under water to obtain real displacements of the water surface
1) Reading data from sensor, converting .dat to .npy
The data is divided into separate format fragments (date, record) containing a fixed number of points.
2) Plotting a graph of pressure fluctuations by day. The number of points included in the construction is noticeably reduced.
Areas corresponding to sensor immersion are highlighted in red.
3) Deleting points that are not wave records. An auxiliary function is immersion intervals
and their graph is built indicating the file name. Clicking on a point on the chart that opens deletes the points before/after.
4) Applying the hydrostatic conversion formula and dividing into 20-minute records, constructing a displacement graph.
You must manually enter the dive depth. The graph can be built several times, recalculation will only be done the first time
starting the program. Deleted days on the x-axis are recalculated.
5) Removal of high frequency components for a stable zero level. Plotting a graph before/after removal.
Because The Fourier transform is an integral and can be broken down into separate
fragments of integration, therefore, to speed up the FT is taken for each fragment.
