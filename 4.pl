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

	% 1. Count repetitions
	% 2. Filter repetitions on the condition
	% 3. Check that there is at least one remaining
	count_repeat(A, Reps),
	include(part2, Reps, Y),
	length(Y, L),
	L > 0.


% Integer to digit array
itoa(N, A) :-
	number_codes(N,X),
	format('~s',[X]),
	maplist(plus(48),A,X).

% Values in the list are increasing
monotone([]) :- true.
monotone([_]) :- true.
monotone([H1, H2 | T]) :-
	H2 >= H1,
	monotone([H2|T]).

% Count repetitions of numbers in a list
% [1,1,2,2,3,4,4,5,5,5] => [2,2,1,2,3]
count_repeat([], []) :- true.
count_repeat([_], [1]) :- true.
count_repeat([H1, H2 | T], [X1 | XT]) :-
	H1 == H2,
	count_repeat([H2 | T], [X | XT]),
	X1 is X + 1.

count_repeat([H1, H2 | T], [1 | XT]) :-
	H1 =\= H2,
	count_repeat([H2 | T], XT).


