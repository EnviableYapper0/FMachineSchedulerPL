machine_time_less_than(machine(_, X, _), Y):-
    X =< Y.

get_time(machine(_,X,_), X).

classify_not_peak([H|T], Y, A, A1, B):-
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
    classify_not_peak(T, Y1, A, Z, B).

classify_not_peak([machine(M, X, N)|_], Y, A, A1, machine(M, Z, N)):-
    append(A1, [machine(M, Y, N)], A),
    Z is X - Y.

classify_machine(X, Y, A, B):-
    classify_not_peak(X, Y, A, [], B).
    
