from chatbot_model import ChatBotModel


if __name__ == '__main__':
    model = ChatBotModel(hadoop_url="http://localhost:51070",
                         hdfs_index_file='/chatbot/bm25_inverted_index.txt', local_index_file='./bm25_inverted_index.txt',
                         corpus_dir='/chatbot/corpus/',
                         unk_answer='抱歉哦，本机器人还不能理解你的问题，要不然换个话题？',
                         max_answer_len=1024)
    model.prepare()
    print("欢迎您与本聊天机器人进行对话，本机器人从经典美剧中学习对话知识，\n"
          "希望您能在对话中获得陪伴和温暖。最后，要注意文明礼貌哦。\n"
          "现在，请您输入第一句话开始我们的聊天吧！")
    quit_query = ['拜拜', '再见', 'Bye']
    while True:
        query = input('>>>')
        if query in quit_query:
            print('<<<欢迎下次再来聊天哦，再见~')
            break
        answer = model.predict_answer(query)
        print(f"<<<{answer}")
