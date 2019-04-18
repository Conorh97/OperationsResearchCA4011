set P1;
set P2;

param payoff {P2, P1};

var Player1 {i in P1} >= 0;
var Player2 {j in P2} >= 0;

var MaxPlayer1;

maximize Player1Objective: MaxPlayer1;
minimize Player2Objective: MaxPlayer1;
	
subject to P1ConstraintA {j in P2}:
	Player2[j] >= 0 complements
		sum {i in P1} payoff[j, i] * Player1[i] >= MaxPlayer1;	
	
subject to P2ConstraintA {i in P1}:
	Player1[i] >= 0 complements	
		sum {j in P2} payoff[j, i] * Player2[j] <= MaxPlayer1; 
	
subject to P1ConstraintB:
	sum {i in P1} Player1[i] = 1;
	
subject to P2ConstraintB:
	sum {j in P2} Player2[j] = 1;


