set PROD;
param production_time {PROD} >= 0;
param profit {PROD} > 0;
param factory_time >= 0;
param minimum_produced {PROD} >= 0;
param efficiency {PROD} > 0;
param fleet_efficiency > 0;

var Produced {p in PROD} >= minimum_produced[p];
var Fleet_Average == (sum {p in PROD} Produced[p] * efficiency[p]) 
					 / (sum {p in PROD} Produced[p]);

maximize Total_Profit: sum {p in PROD} profit[p] * Produced[p];

subject to Time: sum {p in PROD} production_time[p] * Produced[p] <= factory_time;

subject to Min_Efficiency: 
	fleet_efficiency * (sum {p in PROD} Produced[p]) <=
	(sum {p in PROD} efficiency[p] * Produced[p]) ; 
 
 