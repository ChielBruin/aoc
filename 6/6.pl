
orbit(X, Y) :- orbit_direct(X, Y).
orbit(X, Y) :-
  orbit_direct(C, Y),
  orbit(X, C).

orbital_path(X, Y, _, [X, Y]):- orbit_direct(X, Y).
orbital_path(X, Y, _, [Y, X]):- orbit_direct(Y, X).

orbital_path(X, Y, V, [X|A]):-
  (orbit_direct(X, Z); orbit_direct(Z, X)),
  not(member(Z, V)), Z \= Y,
  orbital_path(Z, Y, [X|V], A).


% findall([X,Y], orbit(X,Y), Z), length(Z, L). => 402879
% orbital_path(o_you, o_san, [], Y), length(Y, Z). => 487 => 484 steps
