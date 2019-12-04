% 372304, 847060 => 475
part1(N) :-
	N >= 2.

% 372304, 847060 => 297
part2(N) :-
	N == 2.


password(N1, N2, A) :-
	between(N1, N2, X),
	itoa(X, A),
	monotone(A),
	count_repeat(A, F),
	include(part2, F, B),
	length(B, La),
	La > 0.

itoa(N, A) :-
	number_codes(N,X),
	format('~s',[X]),
	maplist(plus(48),A,X).

monotone([]) :- true.
monotone([_]) :- true.
monotone([H1, H2 | T]) :-
	H2 >= H1,
	monotone([H2|T]).

count_repeat([], []) :- true.
count_repeat([_], [1]) :- true.
count_repeat([H1, H2 | T], [X1 | XT]) :-
	H1 == H2,
	count_repeat([H2 | T], [X | XT]),
	X1 is X + 1.

count_repeat([H1, H2 | T], [1 | XT]) :-
	H1 =\= H2,
	count_repeat([H2 | T], XT).


