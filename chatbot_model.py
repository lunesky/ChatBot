import jieba
from hdfs import Client
import os


class ChatBotModel(object):
    def __init__(self, hadoop_url, hdfs_index_file, local_index_file, corpus_dir, unk_answer='', max_answer_len=1024):
        self.hadoop_url = hadoop_url
        self.hdfs_index_file = hdfs_index_file
        self.local_index_file = local_index_file
        self.corpus_dir = corpus_dir
        self.max_answer_len = max_answer_len
        self.unk_answer = unk_answer
        self.client = None
        self.inverted_index = {}

    def build_connection(self):
        self.client = Client(self.hadoop_url)

    def fetch_index_file(self):
        self.client.download(hdfs_path=self.hdfs_index_file, local_path=self.local_index_file, overwrite=True)

    def load_inverted_index(self):
        with open(self.local_index_file, 'r', encoding='utf-8') as f:
            for line in f:
                word, *querys = line.strip().split('\t')
                for query in querys:
                    file_name, query_id, score = query.split(':')
                    if word in self.inverted_index:
                        self.inverted_index[word].append([file_name, int(query_id), float(score)])
                    else:
                        self.inverted_index[word] = []
                        self.inverted_index[word].append([file_name, int(query_id), float(score)])

    def prepare(self):
        self.build_connection()
        self.fetch_index_file()
        self.load_inverted_index()

    def read_corpus_answer(self, file_name, query_id):
        file_path = os.path.join(self.corpus_dir, file_name)
        file_status = self.client.status(file_path)
        if file_status['length'] <= query_id:
            return None
        with self.client.read(hdfs_path=file_path, offset=query_id,
                           length=self.max_answer_len, encoding='utf-8') as f:
            answer = f.read().strip().split('\n')[0]
            return answer

    def predict_answer(self, query):
        words = jieba.lcut_for_search(query)
        querys = {}
        for word in words:
            if word not in self.inverted_index:
                continue
            for file_name, query_id, score in self.inverted_index[word]:
                query = (file_name, query_id)
                if query in querys:
                    querys[query] += score
                else:
                    querys[query] = score
        if len(querys) == 0:
            return self.unk_answer
        best_query = max(querys.items(), key=lambda x: x[1])
        (best_file_name, best_query_id), best_score = best_query
        best_answer = self.read_corpus_answer(best_file_name, best_query_id)
        if best_answer is None:
            best_answer = self.unk_answer
        return best_answer


