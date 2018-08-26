#-*- coding:utf-8 -*-
# 划分训练集和测试集

import sys
import time
import pandas as pd
import numpy as np

class Division:
    def __init__(self, path):
        self.df = pd.read_csv(path, encoding="gbk")

    # 按照训练集：测试集=3:1划分
    def randomDivision(self):
        # 从一个均匀分布 [ 0, 1 ) 中随机采样，注意定义域是左闭右开，即包含 0 ，不包含 1，长度为数据集长度
        self.df['is_train'] = np.random.uniform(0, 1, len(self.df)) <= .75
        # 划分训练集和测试集
        train, test = self.df[self.df['is_train'] == True], self.df[self.df['is_train'] == False]
        train.to_csv("train_data.csv", encoding="gbk", index=False)  # 写入到csv时，不要将索引写入index = False
        test.to_csv("test_data.csv", encoding="gbk", index=False)  # 写入到csv时，不要将索引写入index = False

    # 按照是否为普通用户划分训练集
    def typeDivision(self):
        train = self.df[self.df['target'] != 0]
        test = self.df[self.df['target'] == 0]
        train.to_csv("train_data.csv", encoding="gbk", index=False)
        test.to_csv("test_data.csv", encoding="gbk", index=False)

    def saveCSV(self, method='random'):
        if method == 'random':
            self.randomDivision()
        if method == 'type':
            self.typeDivision()

# 设置编码
reload(sys)
sys.setdefaultencoding('utf-8')
start =time.clock()
path = 'data.csv'
div = Division(path)
# 传入划分方法以及分界线数据
div.saveCSV('type')
end = time.clock()
print u"任务已完成"
print u"完成时长：" + str(end-start)