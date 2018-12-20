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
