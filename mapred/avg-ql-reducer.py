#!/usr/bin/env python
import sys

query_dict = {}
for line in sys.stdin:
    _, file_name, query_id, query_len = line.strip().split('\t')
    line = f"{file_name}\t{query_id}"
    query_len = eval(query_len)
    query_dict[line] = query_len
query_num = len(query_dict)
query_total = sum(query_dict.values())
avg_query_len = query_total / query_num
print(f'total_query_num\t{query_num}\tavg_query_len\t{avg_query_len}')


