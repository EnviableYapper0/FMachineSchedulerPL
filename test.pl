% male(P) is true when P is male
male(james1).
male(charles1).
male(charles2).
male(james2).
male(george1).

% female(P) is true when P is female
female(catherine).
female(elizabeth).
female(sophia).

% parent(C,P) is true when C has a parent called P
parent(charles1, james1).
parent(elizabeth, james1).
parent(charles2, charles1).
parent(catherine, charles1).
parent(james2, charles1).
parent(sophia, elizabeth).
parent(george1, sophia).

mother(M, P):- 
  female(M),parent(P, M).

sibling(X, Y):-
  parent(X, P), parent(Y, P).

list_sibling(X, List):-
  findall(Y, sibling(X, Y), List).

/*--------------------------------------*/

minimum(X,Y,X) :- X<Y.
minimum(X,Y,Y) :- X>=Y.


size([],0).
size([H|T],N) :- size(T,N1), N is N1+1.


/*------------------------------------------*/

%[machine(2,40,200),machine(1,20,200)] [machine(1,20,100),machine(3,10,100)] [machine(3,10,400)]

% machine(name,kw,minutes)
machine(1,20,300).
machine(2,40,200).
machine(3,10,500).

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

