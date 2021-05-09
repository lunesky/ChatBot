#!/usr/bin/env python
import sys
import math
sys.path.append('./')


k1 = 1
k2 = 1
b = 0.75
with open('avg_query_len', 'r', encoding='utf-8') as f:
    text = f.read().strip().split('\t')
    total_query_num = eval(text[1])
    avg_query_len = eval(text[3])

for line in sys.stdin:
    word, file_name, query_id, query_len, word_count, query_count = line.strip().split('\t')
    tf = word_count / query_len
    df = query_count
    W = math.log2((total_query_num - df + 0.5) / (df + 0.5))
    K = k1 * (1 - b + b * query_len / avg_query_len)
    R = tf * (k1 + 1) / (tf + K)
    score = W * R
    print(f"{word}\t{file_name}\t{query_id}\t{score}")
