let high = 31;
let low = 0;
let done = False;

while not done:
  address = (high + low) / 2;
  search = memory(address); 

  if search == data:
    done = True;
    found = True;
  else if low >= high:
    done = True;
    found = False;
  else if search < data:
    low = address + 1
  else:
    high = address - 1
