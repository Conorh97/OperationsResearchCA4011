param n;
param C;
param points {i in {1 .. 2}, j in {1 .. n}};
param groups {i in {1 .. n}};

var Lambda {1 .. n} >= 0, <= C; 

maximize Objective: -0.5 * sum {i in 1 .. n} Lambda[i] * groups[i] * 
					sum {k in 1 .. 2} points[k, i] *
                    sum {j in 1 .. n} Lambda[j] * groups[j] * points[k, j];

subject to Constraint1: 
	sum {i in 1 .. n} Lambda[i] * groups[i] = 0;
	
