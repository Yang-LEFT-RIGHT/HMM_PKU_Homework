from .Viterbi import Viterbi
import json
from pathlib import Path

def WordSegmentation(sentence):
    ROOT=Path(__file__).resolve().parent.parent.parent
    with open(ROOT/"model/HMM_BMES.json",'r',encoding='utf-8') as f:
        data=json.load(f)
    pi=data['pi']
    A=data['A']
    B=data['B']
    word_pos=Viterbi(sentence,pi,A,B)
    words=[]
    word=""
    for i in range(len(sentence)):
        if word_pos[i]=='S':
            word+=sentence[i]
            words.append(word)
            word=""
        elif word_pos[i]=='E':
            word+=sentence[i]
            words.append(word)
            word=""
        else:
            word+=sentence[i]
    if word:          
        words.append(word)
    return words