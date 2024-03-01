// SPDX-License-Identifier: zlib-acknowledgement
init()
{
  state.lock = lock_create();
  state.cv = cv_create();
  for (int i = 0; i < 10; i += 1)
  {
    RequestID *r_id = &state.request_ids_pool[i];
    r_id->id = i;
    SLL_QUEUE_PUSH(state.first_free_id, state.last_free_id, r_id);

    Request *r = &state.requests[i];
    r->lock = lock_create();
    r->cv = cv_create();
  }

  // For brevity, only check last lock and cv as assume preceeding fail/succeed also
  Request *last_r = &state.requests[9];
  if (last_r->lock == NULL || last_r->cv == NULL)
    panic();
}

finish()
{
  lock_destroy(state.lock);
  cv_destroy(state.cv);
  for (int i = 0; i < 10; i += 1)
  {
    Request *r = &state.requests[i];
    lock_destroy(r->lock);
    cv_destroy(r->cv);
  }
}

send_request()
{
  Request *r = NULL;
  LOCK_SCOPE(state.lock) while (true)
  {
    if (state.first_free_id == NULL)
      wait(state.cv);
    
    RequestID free_id = SLL_QUEUE_POP(first_free_id, last_free_id);
    r = &state.requests[free_id.id];
    r->timestamp = gettime();
    send_immediate_request(r);
    break;
  }

  int value = 0;
  LOCK_SCOPE(r->lock)
  {
    wait(r->cv, r->lock);
    value = r->value;
  }

  LOCK_SCOPE(state.lock)
  {
    RequestID *r_id = &state.request_ids_pool[request_i];
    SLL_QUEUE_PUSH(state.first_free_id, state.last_free_id, r_id);
    cv_signal(state.cv, state.lock);
  }

  return value;
}

recieve_request()
{
  int min_timestamp = INT_MAX;
  int request_i = 0;
  LOCK_SCOPE(state.lock)
  {
    for (int i = 0; i < 10; i += 1)
    {
      Request *r = &state.requests[i];
      if (r->block_num == block_num && r->timestamp < min_timestamp)
      {
        min_timestamp = r->timestamp; 
        request_i = i;
      }
    }
  }

  Request *r = &state.request[request_i]; 
  r->value = value;
  LOCK_SCOPE(r->lock)
  {
    cv_signal(r->cv, r->lock);
  }
}
