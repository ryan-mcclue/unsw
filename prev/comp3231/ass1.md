For counter, one thread could read the counter value before writing to it and then get switched out. 
Another thread could then increment the counter value.
The original thread would then increment an incorrect counter value.
This problem was solved by adding a lock.
Counter operations became atomic by requiring the lock to be acquired and released for their entire scope.

For producerconsumer, the read or write head indexes could be partially read, switched out and returned with incorrect values.
This means a slot in the buffer could be incorrectly overwritten by the producer or duplicated in the consumer.
This problem was solved by encapsulating the data item buffer in a ring struct with a lock and condition variable.
The lock makes producing and consuming atomic.
The conditition variable allows the producer and consumer to wait if no work.
When a consumer finishes, it will broadcast to all producers that work can be done. 
The producers will then wake up, and proceed if there is work to be done.
This same procedure happens vice versa for producer to consumer.

For CDROM, requests have to atomically queued, put to sleep, dequeued and woken up.
A state struct contains an atomic request queue with a lock and condition variable.
The first_free_request_id is a linked list queue that contains indexes to free requests in the queue, allowing for requests can be queued/dequeued in any order.
cdrom_read() will queue a request in the next free slot and remove that request id from the free queue.
A request is set to is_waiting so a cdrom_handler() does not try and wakeup a request that isn't waiting.
The handler will then find a matching block num waiting request and mark it as not waiting.
This prevents no other handler from waking up the same request with the same block_num.
Once cdrom_read() is woken up, it will mark its request slot as free and wakeup any previous calls that are waiting for free requests.
