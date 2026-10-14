# HMM 中文分词

文本挖掘课程作业1：基于隐马尔可夫模型的中文分词。

## 功能

- 训练：从PKU基于1998年人民日报的经典标注语料统计 HMM 参数
- 分词：用 Viterbi 算法对新句子分词

## 环境

```bash
conda env create -f environment.yml
conda activate hmm
```

## 安装

```bash
pip install -e .
```

## 运行

训练：

```bash
python -m scripts.train
```

分词：

```bash
python -m scripts.main
```

## 项目结构

```text
HMM_PKU_Homework1/
├── src/              # 核心代码
│   ├── train/        # 训练相关
│   ├── decode/       # 解码相关
│   └── preprocessing/# 数据预处理
├── scripts/          # 入口脚本
├── data/             # 数据
├── models/           # 训练输出
├── pyproject.toml
├── environment.yml
├── LICENSE
└── README.md
```

## 备注

这个项目不是AI做的！所有AI使用只有部分代码库使用介绍和项目结构建议。