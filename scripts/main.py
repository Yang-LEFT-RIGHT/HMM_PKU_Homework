from src.decode.WordSegmentation import WordSegmentation
from src.decode.PosTagging import PosTagging
import jieba

def main():
    while True:
        mode=input("请输入分词模式（1：jieba分词，2：手写HMM分词）：")
        if mode=="1":
            sentence=input("请输入一个句子：")
            words=list(jieba.cut(sentence))
            print(words)
            pos_pos=PosTagging(words)
            print(pos_pos)
            break
        elif mode=="2":
            sentence=input("请输入一个句子：")
            words=WordSegmentation(sentence)
            print(words)
            pos_pos=PosTagging(words)
            print(pos_pos)
            break
        else:
            print("输入错误")

if __name__ == '__main__':
    main()