param n;
param C;
param points {i in {1 .. 2}, j in {1 .. n}};
param groups {i in {1 .. n}};

var w {i in {1 .. 2}};
var b;

minimize Objective: 1/2 * sum{i in {1 .. 2}} (w[i] ^ 2);

subject to Constraint1 {i in {1 .. n}}: 
	groups[i] * (sum {j in {1 .. 2}} (w[j] * points[j, i]) + b) >= 1;
	
	