set DAYS;
set SCHEDULE;

param min_employees {DAYS} >= 0;
param days_scheduled {DAYS, SCHEDULE} binary;

var Employees {SCHEDULE} >= 0;

minimize Min_Employees: sum {s in SCHEDULE} Employees[s];

subject to Employees_Needed {d in DAYS}:
	sum {s in SCHEDULE} days_scheduled[d,s] * Employees[s] >= min_employees[d];
	