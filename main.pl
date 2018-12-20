/*--------------------------------------
 * helpers
 *--------------------------------------*/

%find minimum of X and Y
minimum(X,Y,X) :- X<Y.
minimum(X,Y,Y) :- X>=Y.

%find minimum of X and Y
size([],0).
size([H|T],N) :- size(T,N1), N is N1+1.


/*--------------------------------------
 * main functions
 *--------------------------------------*/

 % machine(name,kwh,minutes) <-- machine fact
 % machine(1,20,300).
 % machine(2,40,200).
 % machine(3,10,500).

split([], [], [], []).
split([H|T], [H|L1], L2, L3) :- 
  H>=5,H<10, 
  split(T, L1, L2, L3).
split([H|T], L1, [H|L2], L3) :- 
  H<5, 
  split(T, L1, L2, L3).
split([H|T], L1, L2, [H|L3]) :- 
  H>=10,
  split(T, L1, L2, L3).

