from collections import Counter,defaultdict
import json
from pathlib import Path

def HMM_BMES():
    sentences=[]
    sentence=[]
    ROOT=Path(__file__).resolve().parent.parent.parent
    with open(ROOT/"data/pku_training_processed.txt",'r',encoding='utf-8') as f:
        lines=f.readlines()
        lines=[line.strip() for line in lines]
        # 将低频词更换为<UNK>
        word_counter=Counter()
        for line in lines:
            if line=='':
                continue
            word=line.split()[0]
            word_counter[word]+=1
        lines_new=[]
        for line in lines:
            if line=='':
                lines_new.append(line)
                continue
            word=line.split()[0]
            tag=line.split()[1]
            if word_counter[word]<=2:
                line='<UNK> '+tag
            lines_new.append(line)
        lines=lines_new

        for line in lines:
            if line=='':
                if sentence:
                    sentences.append(" ".join(sentence))
                    sentence=[]
            else:
                sentence.append(line)
    chars_sen = [[] for _ in sentences]
    tags_sen = [[] for _ in sentences]
    for i,s in enumerate(sentences):
        chars_sen[i]=[]
        tags_sen[i]=[]
        words=s.split()
        for k,word in enumerate(words):
            if k%2==0:
                chars_sen[i].append(word)
            else:
                tags_sen[i].append(word)
    pi_s=1
    pi_b=1
    pi_e=1
    pi_m=1
    for tags in tags_sen:
        if tags[0]=='S':
            pi_s+=1
        elif tags[0]=='B':
            pi_b+=1
        elif tags[0]=='E':
            pi_e+=1
        elif tags[0]=='M':
            pi_m+=1
    pi_s/=(len(tags_sen)+4)
    pi_b/=(len(tags_sen)+4)
    pi_e/=(len(tags_sen)+4)
    pi_m/=(len(tags_sen)+4)
    print("初始概率如下：")
    print("S:",pi_s,"\nB:",pi_b,"\nE:",pi_e,"\nM:",pi_m,'\n\n')

    A=defaultdict(Counter)
    for tags in tags_sen:
        for i,tag in enumerate(tags):
            if i==len(tags)-1:
                break
            else:
                A[tag][tags[i+1]]+=1
    
    for tag1 in A.keys():
        for tag2 in A.keys():
            A[tag1][tag2]+=1

    for tag in A.keys():
        total=sum(A[tag].values())
        A[tag]={tag:ct/total for tag,ct in A[tag].items()}
    print("转移概率如下：(B对应0,E对应1,M对应2,S对应3)")
    print(A,'\n\n')
    emission_counter=defaultdict(Counter)
    tag_counter=Counter()
    for chars,tags in zip(chars_sen,tags_sen):
        for ch,tag in zip(chars,tags):
            emission_counter[tag][ch]+=1
            tag_counter[tag]+=1
    B={}
    for tag,char_counter in emission_counter.items():
        B[tag]={ch:chct/tag_counter[tag] for ch,chct in char_counter.items()}
    print("发射概率详见文件")

    pi={
        'S':pi_s,
        'B':pi_b,
        'E':pi_e,
        'M':pi_m,
    }
    data={
        'pi':pi,
        'A':A,
        'B':B,
    }
    MODEL_DIR = ROOT/"model"
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_DIR/"HMM_BMES.json",'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=4)
    print("分词器训练完成")