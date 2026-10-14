import numpy as np

def Viterbi(words,pi,A,B):
    labels=B.keys()
    v=[dict() for _ in words]
    p=[dict() for _ in words]

    for pos in labels:
        if B[pos].get(words[0], 0)==0:
            if B[pos].get('<UNK>', 0)!=0:
                v[0][pos]=np.log(pi[pos])+np.log(B[pos]['<UNK>'])
            else:
                v[0][pos]=-np.inf
        else:
            v[0][pos]=np.log(pi[pos])+np.log(B[pos][words[0]])
    for i in range(1,len(words)):
        for pos in labels:
            max_score=-np.inf
            for prev_pos in labels:
                score=v[i-1][prev_pos]+np.log(A[prev_pos][pos])
                if score>max_score:
                    max_score=score
                    p[i][pos]=prev_pos
            if B[pos].get(words[i], 0)==0:
                if B[pos].get('<UNK>', 0)!=0:
                    v[i][pos]=max_score+np.log(B[pos]['<UNK>'])
                else:
                    v[i][pos]=-np.inf
            else:
                v[i][pos]=max_score+np.log(B[pos][words[i]])
    last_scores=v[len(words)-1]
    max_pos=max(last_scores,key=last_scores.get)
    word_pos=[None for _ in words]
    word_pos[-1]=max_pos
    for i in range(len(words)-1,0,-1):
        word_pos[i-1]=p[i][word_pos[i]]
    return word_pos