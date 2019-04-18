set TOWNS;

param distances {TOWNS, TOWNS} >= 0;
param branches >= 0, integer, default 0;

set B {1 .. branches};

var Visited {TOWNS, TOWNS} binary;

minimize Total_Distance: 
	sum {i in TOWNS, j in TOWNS: i != j} distances[i, j] * Visited[i,j];

subject to Successor {i in TOWNS}: 
	sum {j in TOWNS: i != j} Visited[i, j] = 1;

subject to Predecessor {j in TOWNS}: 
	sum {i in TOWNS: i != j} Visited[i, j] = 1;
	
subject to Elim_Branch {k in 1 .. branches}:
	sum{i in B[k], j in TOWNS diff B[k]} Visited[i,j] >= 1;
	






