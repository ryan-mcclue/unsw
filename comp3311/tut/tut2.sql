create table favourites (
  fan text references fans(name),
  player text references players(name),
  primary key (fan, player),
);
