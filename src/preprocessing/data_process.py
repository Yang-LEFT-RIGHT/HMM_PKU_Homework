from pathlib import Path

def data_process():
    ROOT=Path(__file__).resolve().parent.parent.parent
    DATA_DIR = ROOT/"data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR/"pku_training.txt",'r',encoding='utf-8') as f:
        lines=f.readlines()
    lines=[line.strip() for line in lines]
    print("识别到",len(lines),"行数据")
    with open(DATA_DIR/"pku_training_processed.txt",'w',encoding='utf-8',newline='\n') as f:
        for k,line in enumerate(lines):
            words=line.split()
            if len(words)==0:
                continue
            for word in words:
                if len(word)==1:
                    f.write(word+' S'+'\n')
                else:
                    for i,char in enumerate(word):
                        if i==0:
                            f.write(char+' B'+'\n')
                        elif i==len(word)-1:
                            f.write(char+' E'+'\n')
                        else:
                            f.write(char+' M'+'\n')
            if k<len(lines)-1:
                f.write('\n')
            print("[",k+1,"/",len(lines),"]:done")
    print("转换完成")
