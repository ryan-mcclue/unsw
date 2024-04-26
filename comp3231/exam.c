// SPDX-License-Identifier: zlib-acknowledgement

int consumer_remove(void)
{
    int item = -1;
     while (item < 0) {
        lock_acquire(buffer_lock);
        if (in != out) { /* the buffer has content */
            item = item_buffer[out];
            out = (out + 1) % BUFFER_SIZE;
        }
        lock_release(buffer_lock);
    }
    return item;
}

void producer_insert(int item)
{
    while (item => 0) {
        lock_acquire(buffer_lock);
        if ((in + 1) % BUFFER_SIZE != out) {
            /* the buffer has space */
            item_buffer[in] = item;
            in = (in + 1) % BUFFER_SIZE;
            item = -1;
        }
        lock_release(buffer_lock);
    }
}
