#!/usr/bin/env python
import sys


curr_word = None
curr_count = 0
for line in sys.stdin:
    word, file_name, query_id, query_len, count = line.strip().split('\t')
    word = f"{word}\t{file_name}\t{query_id}\t{query_len}"
    count = eval(count)
    if curr_word is None:
        curr_word = word
        curr_count = count
    elif curr_word == word:
        curr_count += count
    else:
        print(f"{curr_word}\t{curr_count}")
        curr_word = word
        curr_count = count

if curr_word is not None:
    print(f"{curr_word}\t{curr_count}")