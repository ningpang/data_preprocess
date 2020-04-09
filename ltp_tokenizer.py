# -*- coding: utf-8 -*-
import os
LTP_DATA_DIR = './ltp_data'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, './Baike/all_entity.txt')  # 加载模型
f1 = open('./Baike/train.txt')
f2 = open('./Baike/train_ltp.txt', 'a')
count = 0
while True:
    content = f1.readline()
    if content == '':
        break
    content = content.strip().split()
    ent1 = content[0]
    ent2 = content[1]
    rel = content[4]
    sent = ''
    for i in content[5:]:
        sent += i
    words = segmentor.segment(sent)  # 分词
    if ent1 not in words:
        count += 1
    if ent2 not in words:
        count += 1
    sentence = '\t'.join(words)
    f2.write(ent1+'\t'+ent2+'\t'+ent1+'\t'+ent2+'\t'+rel+'\t'+sentence+'\n')
    # break
print(count)