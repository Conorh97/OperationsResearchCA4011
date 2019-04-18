set TOWNS;

param distances {TOWNS, TOWNS} >= 0;

var Radii {TOWNS} >= 0;

maximize Total_Distance: 
	sum {i in TOWNS} 2 * Radii[i];

subject to DistanceBounds {i in TOWNS, j in TOWNS: i != j}: 
	Radii[i] + Radii[j] <= distances[i, j];
	
subject to NotZero {i in TOWNS}:
	Radii[i] >= 0;
