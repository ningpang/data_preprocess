from numpy import *
import numpy as np
import re
import json

f1 = open('example.txt')
f2 = open('example_parser.txt')
number = 0
path_flag = 1
count_UNK = 0
def find_path(word1, word2, graph, relation):
    path = [word2]
    dp_rel = []
    beg = word2
    while True:
        arr = list(graph[beg])
        head = max(arr)
        if head < 1:
            break
        idx = arr.index(max(arr))
        path.append(idx)
        dp_rel.append(relation[beg][idx])
        if idx == word1:
            break
        beg = idx
    if path[-1] == word1:
        return path, dp_rel
    else:
        return [], []
def save_path(path1, dr1, path2, dr2, sentence, relset, pos):
    sp_w = ''
    sp_r = ''
    sp_p = ''
    sp_d = ''
    for i in range(len(path1)):
        if i < len(path1)-1:
            sp_w += sentence[path1[i]]+' '
            sp_r += relset[dr1[i]]+' '
            sp_p += pos[path1[i]]+' '
            sp_d += '0 '
        else:
            sp_w += sentence[path1[i]] + ' '
            sp_r += 'INTER '
            sp_p += pos[path1[i]] + ' '
            sp_d += '1 '
    if path1 != []:
        for i in range(len(dr2)):
            sp_w += sentence[path2[i+1]] + ' '
            sp_r += relset[dr2[i]] + ' '
            sp_p += pos[path2[i+1]] + ' '
            sp_d += '2 '
    else:
        for i in range(len(path2)):
            if i == 0:
                sp_w += sentence[path2[i]] + ' '
                sp_r += 'INTER '
                sp_p += pos[path2[i]] + ' '
                sp_d += '1 '
            else:
                sp_w += sentence[path2[i]] + ' '
                sp_r += relset[dr2[i-1]] + ' '
                sp_p += pos[path2[i]] + ' '
                sp_d += '2 '
    return sp_w, sp_r, sp_p, sp_d
have = 0
data = []
s_id = 0
while True:
    # get enetity pair and tokens
    s_id += 1
    print(s_id)
    entity = f1.readline()
    if entity == '':
        break
    content = entity.strip().split()
    e1 = content[0]
    e2 = content[1]

    ins = ''
    for w in content[5:]:
        ins += w+' '
    # get the dependency relation
    pos = f2.readline()
    pos = pos.split()
    sen_s = ''
    for t in pos:
        sen_s += t+' '
    sentence = ['ROOT'] + content[5:]
    pos = ['root'] + pos
    dp_relation = f2.readline()
    dp_relation = dp_relation.strip().split()

    instance = {}
    instance['MDP_w'] = []
    instance['MDP_r'] = []
    instance['MDP_d'] = []
    instance['MDP_p'] = []
    # store the graph and relation
    graph_store = zeros((700, 700), int16)
    relation_store = zeros((700, 700), int16)

    k = 1
    relset = []
    rel2id = {}
    dic = {}
    for i, word in enumerate(sentence):
        dic[word] = i

    for i, item in enumerate(dp_relation):
        #get the relation
        item = item.split(':')
        word = int(item[0])
        rel = item[1]
        graph_store[i+1][word] = 1
        if rel not in relset:
            relset.append(rel)
            rel2id[rel] = len(relset)-1
        relation_store[i+1][word] = rel2id[rel]
    id1 = dic[e1]
    id2 = dic[e2]
    root = dic['ROOT']
    flag = 0
    instance['head'] = {}
    instance['tail'] = {}
    instance['head']['word'] = e1
    instance['head']['id'] = e1
    instance['tail']['word'] = e2
    instance['tail']['id'] = e2
    instance['relation'] = content[4]
    instance['sentence'] = ins
    instance['sen_pos'] = sen_s
    w = []
    r = []
    p = []
    d = []
    rootverb = list(graph_store[:, 0])
    idx = rootverb.index(max(rootverb))
    instance['Root'] = sentence[idx]
    for item in sentence[1:]:
        e12root, d_r1 = find_path(dic[item], id1, graph_store, relation_store)
        root2e2, d_r2 = find_path(dic[item], id2, graph_store, relation_store)
        if e12root == [] and root2e2 == []:
            continue
        have += 1
        root2e2.reverse()
        d_r2.reverse()
        # print(e12root, root2e2)
        sp_w, sp_r, sp_p, sp_d= save_path(e12root, d_r1, root2e2, d_r2, sentence, relset, pos)
        have += 1
        w.append(sp_w)
        r.append(sp_r)
        p.append(sp_p)
        d.append(sp_d)

    if len(w) > 7:
        # print(list(range(len(w))))
        sample = random.choice(list(range(len(w))), 7)
        for index in sample:
            instance['MDP_w'].append(w[index])
            instance['MDP_r'].append(r[index])
            instance['MDP_d'].append(d[index])
            instance['MDP_p'].append(p[index])
    else:
        instance['MDP_w'] = w
        instance['MDP_r'] = r
        instance['MDP_d'] = d
        instance['MDP_p'] = p

    data.append(instance)

with open('./valid.json', 'w') as dump_f:
    json.dump(data, dump_f)
