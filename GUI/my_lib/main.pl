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

% find_greater_machine by kw
find_greater(machine(N,Kw1,M),machine(_,Kw2,_),machine(N,Kw1,M)) :-
  Kw1 >= Kw2.
find_greater(machine(_,Kw1,_),machine(N,Kw2,M),machine(N,Kw2,M)) :-
  Kw1 < Kw2.

is_less_than(machine(_, Kw1, _), machine(N,Kw2,M)):-
    Kw1 < Kw2.

pivoting(H,[],[],[]).
pivoting(H,[X|T],[X|L],G):- 
    is_less_than(X, H),
    pivoting(H,T,L,G).
pivoting(H,[X|T],L,[X|G]):- 
    pivoting(H,T,L,G).

machine_sort(List,Sorted):-q_sort(List,[],Sorted).
q_sort([],Acc,Acc).
q_sort([H|T],Acc,Sorted):-
	pivoting(H,T,L1,L2),
	q_sort(L1,Acc,Sorted1),q_sort(L2,[H|Sorted1],Sorted).

% split a list into 3 lists on conditions
% split([], [], [], []).
% split([H|T], [H|L1], L2, L3) :- 
%   H>=5,H<10, 
%   split(T, L1, L2, L3).
% split([H|T], L1, [H|L2], L3) :- 
%   H<5, 
%   split(T, L1, L2, L3).
% split([H|T], L1, L2, [H|L3]) :- 
%   H>=10,
%   split(T, L1, L2, L3).

% split a list into 3 lists on conditions
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

