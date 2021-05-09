#!/usr/bin/env python
import sys


for line in sys.stdin:
    word, file_name, query_id, query_len, word_count, query_count = line.strip().split('\t')
    print(f"lineLen\t{file_name}\t{query_id}{query_len}")

