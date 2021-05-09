#!/usr/bin/env python
import sys


top = 10
curr_word = None
curr_query_list = {}
for line in sys.stdin:
    word, file_name, query_id, score = line.strip().split('\t')
    query = f"{file_name}:{query_id}"
    score = eval(score)
    if curr_word is None:
        curr_word = word
        curr_query_list[query] = score
    elif curr_word == word:
        curr_query_list[query] = score
    else:
        top_querys = sorted(curr_query_list.items(), key= lambda x: x[1], reverse=True)[:top]
        top_querys = [f"{item[0]}:{item[1]}" for item in top_querys]
        top_querys = '\t'.join(top_querys)
        print(f"{curr_word}\t{top_querys}")
        curr_word = word
        curr_query_list = {query: score}
if curr_word is not None:
    top_querys = sorted(curr_query_list.items(), key=lambda x: x[1], reverse=True)[:top]
    top_querys = [f"{item[0]}:{item[1]}" for item in top_querys]
    top_querys = '\t'.join(top_querys)
    print(f"{curr_word}\t{top_querys}")


