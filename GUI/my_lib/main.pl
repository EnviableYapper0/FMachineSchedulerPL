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
 * main functions
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


% classify machine into each peak
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
