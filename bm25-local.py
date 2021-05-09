import jieba
import os
import math


def get_word_count(corpus_dir):
    word_count = {}
    query_num = 0
    query_total_len = 0
    corpus_files = os.listdir(corpus_dir)
    for file in corpus_files:
        file_path = os.path.join(corpus_dir, file)
        query_id = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                query_num += 1
                query_id += len(line.encode())
                words = jieba.lcut_for_search(line.strip())
                query_len = len(words)
                query_total_len += query_len
                for word in words:
                    word_query = (word, file, query_id, query_len)
                    if word_query in word_count:
                        word_count[word_query] += 1
                    else:
                        word_count[word_query] = 1
    return word_count, query_num, query_total_len / query_num


def get_word_query_count(word_count):
    word_query_count = {}
    for word, file, query_id, query_len in word_count.keys():
        if word in word_query_count:
            word_query_count[word] += 1
        else:
            word_query_count[word] = 1
    return word_query_count


def get_bm25_score(word_count, word_query_count, query_total_num,  query_avg_len, k1 = 1, b = 0.75):
    word_bm25_score = {}
    for (word, file, query_id, query_len), word_num in word_count.items():
        query_num = word_query_count[word]
        tf = word_num / query_len
        df = query_num
        W = math.log2((query_total_num - df + 0.5) / (df + 0.5))
        K = k1 * (1 - b + b * query_len / query_avg_len)
        R = tf * (k1 + 1) / (tf + K)
        score = W * R
        word_bm25_score[(word, file, query_id)] = score
    return word_bm25_score


def get_inverted_index(word_bm25_score, top=30):
    inverted_index = {}
    for (word, file, query_id), score in word_bm25_score.items():
        if word in inverted_index:
            inverted_index[word].append((file, query_id, score))
        else:
            inverted_index[word] = [(file, query_id, score)]
    inverted_index_top = {}
    for word, score_list in inverted_index.items():
        top_list = sorted(score_list, key=lambda x: x[2], reverse=True)[:top]
        inverted_index_top[word] = top_list
    return inverted_index_top

def store_inverted_index(inverted_index_top, index_file):
    with open(index_file, 'w', encoding='utf-8') as f:
        for word, top_list in inverted_index_top.items():
            top_list_str = '\t'.join([':'.join([str(i) for i in item]) for item in top_list])
            word_index_str = '\t'.join([word, top_list_str])
            f.write(word_index_str + '\n')

if __name__ == "__main__":
    corpus_dir = './corpus'
    index_file = './bm25_inverted_index.txt'
    word_count, query_total_num, query_avg_len = get_word_count(corpus_dir=corpus_dir)
    word_query_count = get_word_query_count(word_count=word_count)
    word_bm25_score = get_bm25_score(word_count=word_count, word_query_count=word_query_count,
                                     query_total_num=query_total_num,  query_avg_len=query_avg_len)
    inverted_index_top = get_inverted_index(word_bm25_score=word_bm25_score)
    store_inverted_index(inverted_index_top=inverted_index_top, index_file=index_file)









