machine_time_less_than(machine(_,_,X), Length):-
    X =< Length.

get_time(machine(_,_,X), X).

classify_not_peak([H|T], NonPeakLength, PeakLength, NonPeakList, NonPeakAcc, PeakList, CritialPeakList):-
    get_time(H, X),
    machine_time_less_than(H, NonPeakLength),
    !,

    NewLength is NonPeakLength - X,
    append(NonPeakAcc, [H], NewAcc),
    classify_not_peak(T, NewLength, PeakLength, NonPeakList, NewAcc, PeakList, CritialPeakList).

classify_not_peak([machine(MID, KWh, X)|T], NonPeakLength, PeakLength, NonPeakList, NonPeakAcc, PeakList, CritialPeakList):-
    print(a),
    append(NonPeakAcc, [machine(MID, KWh, NonPeakLength)], NonPeakList),
    print(a),
    append([machine(MID, KWh, NewMachineLength)], T, L),
    NewMachineLength is X - NonPeakLength,
    classify_peak(L, PeakLength, PeakList, [], CritialPeakList).

classify_peak([H|T], PeakLength, PeakList, PeakAcc, CritialPeakList):-
    get_time(H, X),
    machine_time_less_than(H, PeakLength),
    !,

    print(b),
    NewLength is PeakLength - X,
    append(PeakAcc, [H], NewAcc),
    classify_peak(T, NewLength, PeakList, NewAcc, CritialPeakList).

classify_peak([machine(MID, KWh, X)|T], PeakLength, PeakList, PeakAcc, [machine(MID, KWh, NewMachineLength)|T]):-
    append(PeakAcc, [machine(MID, KWh, PeakLength)], PeakList),
    print(c),
    NewMachineLength is X - PeakLength.

classify_machine(List, NonPeakLength, PeakLength, NonPeakList, PeakList, CritialPeakList):-
    classify_not_peak(List, NonPeakLength, PeakLength, NonPeakList, [], PeakList, CritialPeakList).
