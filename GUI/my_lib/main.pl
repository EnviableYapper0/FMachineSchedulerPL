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
 * Sorting
 *--------------------------------------*/

 % machine(name,minutes,kwh) <-- machine fact
 % machine(1,20,300).
 % machine(2,40,200).
 % machine(3,10,500).

% find_less_machine by kw
is_less_than(machine(_, _, Kw1), machine(_, _, Kw2)):-
    Kw1 < Kw2.

% sort machine by kwh
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


/*--------------------------------------
 * Classify machine into each peak
 *--------------------------------------*/
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
    !,
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

classify_peak([machine(MID, X, KWh)|T], PeakLength, PeakList, PeakAcc, [machine(MID, NewMachineLength, KWh)|T]):-
    !,
    append(PeakAcc, [machine(MID, PeakLength, KWh)], PeakList),
    NewMachineLength is X - PeakLength.

classify_peak(L, _, PeakList, Acc, []):-
    !,
    append(Acc, L, PeakList).

classify_machine(List, NonPeakLength, PeakLength, NonPeakList, PeakList, CritialPeakList):-
    classify_not_peak(List, NonPeakLength, PeakLength, NonPeakList, [], PeakList, CritialPeakList).


/*--------------------------------------
 * Create time table
 *--------------------------------------*/

arrange_nonpeak_machine(L, [], Acc, B, C, CurrentTime):-
    PeakStart is 540,
    arrange_peak_machine(L, [], Acc, B, C, PeakStart).

arrange_nonpeak_machine(L, A, Acc, B, C, CurrentTime):-
    PeakStart is 540,
    CurrentTime > PeakStart,
    arrange_peak_machine(L, A, Acc, B, C, CurrentTime).

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
    append(Acc, [sorted_machine(M, Z, N, PeakStart, CurrentTime)], NewAcc),
    arrange_peak_machine(L, [machine(M, Z1, N)|T], NewAcc, B, C, PeakStart).

arrange_peak_machine(L, A, Acc, B, C, CurrentTime):-
    CriticalPeakStart is 810,
    CurrentTime > CriticalPeakStart,
    arrange_critical_machine(L, A, Acc, B, C, CurrentTime).

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

