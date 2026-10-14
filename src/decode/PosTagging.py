from .Viterbi import Viterbi
import json
from pathlib import Path

def PosTagging(words):
    ROOT=Path(__file__).resolve().parent.parent.parent
    with open(ROOT/"model/HMM_POS.json",'r',encoding='utf-8') as f:
        data=json.load(f)
    pi=data['pi']
    A=data['A']
    B=data['B']
    pos_pos=Viterbi(words,pi,A,B)
    return pos_pos