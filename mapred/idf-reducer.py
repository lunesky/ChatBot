#!/usr/bin/env python
import sys


curr_word = None
curr_count = 0
word_querys = []
for line in sys.stdin:
    word, file_name, query_id, query_len, word_count, query_count = line.strip().split('\t')
    word_query = f"{word}\t{file_name}\t{query_id}\t{query_len}\t{word_count}"
    count = eval(query_count)
    if curr_word is None:
        curr_word = word
        curr_count = count
        word_querys.append(word_query)
    elif curr_word == word:
        curr_count += count
        word_querys.append(word_query)
    else:
        for wd in word_querys:
            print(f"{wd}\t{curr_count}")
        curr_word = word
        curr_count = count
        word_querys = [word_query]

if curr_word is not None:
    for wd in word_querys:
        print(f"{wd}\t{curr_count}")