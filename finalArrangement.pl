arrange_nonpeak_machine(L, [], Acc, B, C, CurrentTime):-
    PeakStart is 540,
    arrange_peak_machine(L, [], Acc, B, C, PeakStart).

arrange_nonpeak_machine(L, [machine(M, X, N)|T], Acc, B, C, CurrentTime):-
    PeakStart is 540,
    NewTime is CurrentTime + X,
    NewTime =< PeakStart,
    !,
    append(Acc, [sorted_machine(M, X, N, CurrentTime, NewTime)], NewAcc),
    arrange_nonpeak_machine(L, T, NewAcc, B, C, NewTime).

arrange_nonpeak_machine(L, [machine(M, X, N)|T], Acc, B, C, CurrentTime):-
    PeakStart is 540,
    Z is PeakStart - CurrentTime,
    Z1 is X - Z,
    append(Acc, [sorted_machine(M, Z, N, PeakStart, CurrentTime, PeakStart)], NewAcc),
    arrange_peak_machine(L, [machine(M, Z1, N)|T], NewAcc, B, C, PeakStart).

arrange_peak_machine(L, A, Acc, [], C, CurrentTime):-
    CriticalPeakStart is 810,
    arrange_critical_machine(L, A, Acc, [], C, CriticalPeakStart).

arrange_peak_machine(L, A, Acc, [machine(M, X, N)|T], C, CurrentTime):-
    CriticalPeakStart is 810,
    NewTime is CurrentTime + X,
    NewTime =< CriticalPeakStart,
    !,
    append(Acc, [sorted_machine(M, X, N, CurrentTime, NewTime)], NewAcc),
    arrange_peak_machine(L, A, NewAcc, T, C, NewTime).

arrange_peak_machine(L, A, Acc, [machine(M, X, N)|T], C, CurrentTime):-
    CriticalPeakStart is 810,
    Z is CriticalPeakStart - CurrentTime,
    Z1 is X - Z,
    append(Acc, [sorted_machine(M, Z1, N, CurrentTime, CriticalPeakStart)], NewAcc),
    arrange_critical_machine(L, A, NewAcc, [machine(M, Z, N)|T], C, CriticalPeakStart).

arrange_critical_machine(L, A, Acc, B, [machine(M, X, N)|T], CurrentTime):-
    CriticalPeakEnd is 930,
    NewTime is CurrentTime +  X,
    !,
    append(Acc, [sorted_machine(M, X, N, CurrentTime, NewTime)], NewAcc),
    arrange_critical_machine(L, A, NewAcc, B, T, NewTime).

arrange_critical_machine(L, A, Acc, B ,[], _):-
    CriticalPeakEnd is 930,
    arrange_peak_machine(L, A, Acc, B, CriticalPeakEnd).

arrange_peak_machine(L, A, Acc, [machine(M, X, N)|T], CurrentTime):-
    NewTime is CurrentTime + X,
    !,
    append(Acc, [sorted_machine(M, X, N, CurrentTime, NewTime)], NewAcc),
    arrange_peak_machine(L, A, NewAcc, T, NewTime).

arrange_peak_machine(L, A, Acc, [], _):-
    PeakEnd is 1320,
    arrange_nonpeak_machine(L, A, Acc, PeakEnd).

arrange_nonpeak_machine(L, [machine(M, X, N)|T], Acc, CurrentTime):-
    NewTime is CurrentTime + X,
    !,
    append(Acc, [sorted_machine(M, X, N, CurrentTime, NewTime)], NewAcc),
    arrange_nonpeak_machine(L, T, NewAcc, NewTime).

arrange_nonpeak_machine(L, [], L, _).
    

final_arrangement(L, A, B, C, CurrentTime):-
    arrange_nonpeak_machine(L, A, [], B, C, CurrentTime).
