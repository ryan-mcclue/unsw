create trigger pk_check before insert or update on R
for each row execute pk_check_trig();

create function pk_check_trig() returns trigger as $$
begin

end;
$$ language plpgsql;

create aggregate my_avg(numeric) (
  stype = Pair,
  initcond = (0,0),
  sfunc = my_avg_func,
  finalfunc = my_avg_norm
);

create type Pair as (counter numeric, amt integer);
create function my_avg_func(state Pair, next numeric) returns Pair
as $$
begin
  state.counter := state.counter + 1;
  state.amt := state.amt + next;
  return s;
end;
$$

create function my_avg_norm(state Pair) returns numeric
as $$
begin
  return state.amt::numeric / state.counter::numeric; -- overcome integer truncation
end;
$$ 
