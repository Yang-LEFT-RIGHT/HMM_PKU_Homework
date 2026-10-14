from collections import Counter,defaultdict
import json
from pathlib import Path

def HMM_POS():
    ROOT=Path(__file__).resolve().parent.parent.parent
    with open(ROOT/"data/1998-01-2003版-带音.txt",'r',encoding='utf-8') as f:
        lines=f.readlines()
        lines=[line.strip() for line in lines]
    words_sen=[[] for _ in lines]
    for i,line in enumerate(lines):
        words_sen[i]=line.split()
    # 由于每一行开头都是一个固定时间，这会影响训练效果（因为每个句首词性都是一样的），所以统一删掉各行第一个词
    for words in words_sen:
        if len(words)==0:
            continue
        del words[0]
    pi=Counter()
    word_counter=Counter()
    pos_couter=Counter()
    for words in words_sen:
        if len(words)==0:
            continue
        for word in words:
            ch=word.split('/')[0]
            pos=word.split('/')[1]
            word_counter[ch]+=1
            pos_couter[pos]+=1
    words_sen_new=[]
    for words in words_sen:
        words_new=[]
        if len(words)==0:
            words_sen_new.append([])
            continue
        for word in words:
            ch=word.split('/')[0]
            pos=word.split('/')[1]
            if word_counter[ch]<=3:
                words_new.append('<UNK>/'+pos)
                continue
            else:
                words_new.append(word)
        words_sen_new.append(words_new)
    words_sen=words_sen_new
    
    for pos in pos_couter.keys():
        pi[pos]+=1

    for words in words_sen:
        if len(words)==0:
            continue
        pos=words[0].split('/')[1]
        pi[pos]+=1
    pi={pos:ct/(len(words_sen)+len(pos_couter.keys())) for pos,ct in pi.items()}
    print("初始概率完成")
    #print(pi)

    A=defaultdict(Counter)

    for pos in pos_couter.keys():
        for next_pos in pos_couter.keys():
            A[pos][next_pos]+=1

    for words in words_sen:
        if len(words)==0:
            continue
        for i in range(len(words)-1):
            pos=words[i].split('/')[1]
            next_pos=words[i+1].split('/')[1]
            A[pos][next_pos]+=1
    for pos in A.keys():
        total=sum(A[pos].values())
        A[pos]={pos:ct/total for pos,ct in A[pos].items()}
    print("转移概率完成")
    #print(A)
    B=defaultdict(Counter)
    for words in words_sen:
        if len(words)==0:
            continue
        for word in words:
            pos=word.split('/')[1]
            word=word.split('/')[0]
            B[pos][word]+=1
    V_num=len(word_counter)+1
    for pos in B.keys():
        total=sum(B[pos].values())
        B[pos]={word:(ct+1)/(total+V_num) for word,ct in B[pos].items()}
        B[pos]['<UNK>']=1/(total+V_num)
    print("发射概率完成")
    MODEL_DIR = ROOT/"model"
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_DIR/"HMM_POS.json",'w',encoding='utf-8') as f:
        json.dump({'pi':pi,'A':A,'B':B},f,ensure_ascii=False,indent=4)
    print("词性标注器训练完成")
