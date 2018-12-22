machine_time_less_than(machine(_,X,_), Length):-
    X =< Length.

get_time(machine(_,X,_), X).

classify_not_peak([H|T], NonPeakLength, PeakLength, NonPeakList, NonPeakAcc, PeakList, CritialPeakList):-
    get_time(H, X),
    machine_time_less_than(H, NonPeakLength),
    !,

    NewLength is NonPeakLength - X,
    append(NonPeakAcc, [H], NewAcc),
    classify_not_peak(T, NewLength, PeakLength, NonPeakList, NewAcc, PeakList, CritialPeakList).

classify_not_peak([machine(MID, X, KWh)|T], NonPeakLength, PeakLength, NonPeakList, NonPeakAcc, PeakList, CritialPeakList):-
    append(NonPeakAcc, [machine(MID, NonPeakLength, KWh)], NonPeakList),
    append([machine(MID, NewMachineLength, KWh)], T, L),
    NewMachineLength is X - NonPeakLength,
    classify_peak(L, PeakLength, PeakList, [], CritialPeakList).

classify_not_peak(L, _, _, NonPeakList, Acc, [], []):-
    !,
    append(Acc, L, NonPeakList).

classify_peak([H|T], PeakLength, PeakList, PeakAcc, CritialPeakList):-
    get_time(H, X),
    machine_time_less_than(H, PeakLength),
    !,

    NewLength is PeakLength - X,
    append(PeakAcc, [H], NewAcc),
    classify_peak(T, NewLength, PeakList, NewAcc, CritialPeakList).

classify_peak(L, _, PeakList, Acc, []):-
    !,
    append(Acc, L, PeakList).

classify_peak([machine(MID, X, KWh)|T], PeakLength, PeakList, PeakAcc, [machine(MID, NewMachineLength, KWh)|T]):-
    append(PeakAcc, [machine(MID, PeakLength, KWh)], PeakList),
    NewMachineLength is X - PeakLength.

classify_machine(List, NonPeakLength, PeakLength, NonPeakList, PeakList, CritialPeakList):-
    classify_not_peak(List, NonPeakLength, PeakLength, NonPeakList, [], PeakList, CritialPeakList).
