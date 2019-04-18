set ORIG;
set DEST;

param supply {ORIG} >= 0;
param demand {DEST} >= 0;

	check: sum {i in ORIG} supply[i] = sum {j in DEST} demand[j];
	
param cost {ORIG,DEST} >= 0;
var Trans {ORIG,DEST} >= 0;

minimize Pref_of {i in ORIG}:
	sum {j in DEST} cost[i,j] * Trans[i,j];	

minimize Total_Cost:
	sum {i in ORIG, j in DEST} cost[i,j] * Trans[i,j];
	
subject to Supply {i in ORIG}:
	sum {j in DEST} Trans[i,j] = supply[i];
	
subject to Demand {j in DEST}:
	sum {i in ORIG} Trans[i,j] = demand[j];
	
subject to Stay_Optimal:
	28 <= sum {i in ORIG, j in DEST} cost[i,j] * Trans[i,j] <= 30;
	
