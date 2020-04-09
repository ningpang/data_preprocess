# -*- coding: utf-8 -*-
import os
LTP_DATA_DIR = './ltp_data'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
# segmentor.load_with_lexicon(cws_model_path, './GitLink/all_entity.txt')  # 加载模型
from pyltp import Postagger
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型
from pyltp import Parser
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型

# sent = '国务院总理李克强调研上海外高桥时提出，支持上海积极探索新机制。'
f1 = open('example.txt')
f2 = open('example_parser.txt', 'a')
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
#     # words = segmentor.segment(sent)  # 分词
    postags = postagger.postag(content[5:])
    arcs = parser.parse(content[5:], postags)
    tag = '\t'.join(postags)
    dp = "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
    f2.write(tag+'\n'+dp+'\n')
    print(tag, dp)
    print(content[5:])
segmentor.release()  # 释放模型
postagger.release()  # 释放模型
parser.release()  # 释放模型