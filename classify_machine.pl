machine_time_less_than(machine(_, X, _), Y):-
    X =< Y.

get_time(machine(_,X,_), X).

classify_not_peak([H|T], Y1, Y2, A, A1, B, C):-
    get_time(H, X),
    machine_time_less_than(H, Y1),
    !,    

    Y is Y1 - X,
    append(A1, [H], Z),
    classify_not_peak(T, Y, Y2, A, Z, B, C).

classify_not_peak([machine(M, X, N)|T], Y1, Y2, A, A1, B, C):-
    append(A1, [machine(M, Y1, N)], A),
    append([machine(M, Z, N)], T, L),
    Z is X - Y1,
    classify_peak(L, Y2, B, [], C).

classify_peak([H|T], Y2, B, B1, C):-
    get_time(H, X),
    machine_time_less_than(H, Y2),
    !,
    Y is Y2 - X,
    append(B1, [H], Z),
    classify_peak(T, Y, B, Z, C).

classify_peak([machine(M, X, N)|T], Y2, B, B1, [machine(M, Z, N)]):-
    append(B1, [machine(M, Y2, N)], B),
    % append([machine(M, Z, N)], T, C]),
    print(T),
    Z is X - Y2.

classify_machine(X, Y1, Y2, A, B, C):-
    classify_not_peak(X, Y1, Y2, A, [], B, C).
