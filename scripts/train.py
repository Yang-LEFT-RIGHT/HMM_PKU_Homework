from src.train.HMM_BMES import HMM_BMES
from src.train.HMM_POS import HMM_POS
from src.preprocessing.data_process import data_process

if __name__ == "__main__":
    print("开始处理数据")
    data_process()
    print("开始训练HMM_BMES")
    HMM_BMES()
    print("开始训练HMM_POS")
    HMM_POS()
    print("所有训练完毕")