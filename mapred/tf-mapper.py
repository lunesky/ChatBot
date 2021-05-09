#!/usr/bin/env python
import sys
import zipimport
import os
sys.path.append('./')
importer = zipimport.zipimporter('jieba.mod')
jieba = importer.load_module('jieba')
import jieba


query_id = 0
file_name = os.getenv("map_input_file")
path, file_name = os.path.split(file_name)
for line in sys.stdin:
    query_id += len(line)
    line = line.strip()
    words = jieba.lcut_for_search(line)
    query_len = len(words)
    for word in words:
        print(f"{word}\t{file_name}\t{query_id}\t{query_len}\t1")

