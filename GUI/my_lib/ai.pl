extend([Node|Path],NewPaths) :-
    findall([NewNode,Node|Path],
            (path(Node,NewNode,_),
            \+ member(NewNode,Path)),
            NewPaths).

path_cost([A,B],Cost) :-
    path(A,B,Cost).
path_cost([A,B|T],Cost) :-
    path(A,B,Cost1),
    path_cost([B|T],Cost2),
    Cost is Cost1+Cost2.

reverse_path_cost([A,B],Cost) :-
    path(B,A,Cost).
reverse_path_cost([A,B|T],Cost) :-
    path(B,A,Cost1),
    reverse_path_cost([B|T],Cost2),
    Cost is Cost1+Cost2.

sort_queue(L,L2) :-
    swap(L,L1), !,
    sort_queue(L1,L2).
sort_queue(L,L).

swap([X,Y|T],[Y,X|T]) :-
    reverse_path_cost(X,CX),
    reverse_path_cost(Y,CY),
    CX>CY.
swap([X|T],[X|V]) :-
    swap(T,V).

uni_cost([[Goal|Path]|_],Goal,[Goal|Path],0).
uni_cost([Path|Queue],Goal,FinalPath,N) :-
    extend(Path,NewPaths),
    append(Queue,NewPaths,Queue1),
    sort_queue(Queue1,NewQueue),
    uni_cost(NewQueue,Goal,FinalPath,M),
    N is M+1.

find_cheapest_path(Path):-
    uni_cost([[start]], end, Path, _).