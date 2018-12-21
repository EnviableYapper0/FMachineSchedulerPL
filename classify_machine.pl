machine_time_less_than(machine(_, X, _), Y):-
    X =< Y.

get_time(machine(_,X,_), X).

classify_not_peak([H|T], Y, A, A1):-
    get_time(H, X),
    print(a),
    print(X),
    print(b),
    print(Y),
    print(c),
    machine_time_less_than(H, Y),
    
    Y1 is Y - X,
    append(A1, [H], Z),
    print(Z),
    classify_not_peak(T, Y1, A, Z).

classify_not_peak([machine(M, X, Z)|_], Y, [A|machine(M, Y, Z)], A).

classify_machine(X, Y, A):-
    classify_not_peak(X, Y, A, []).
    
