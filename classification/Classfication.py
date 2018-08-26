#-*- coding:utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, ShuffleSplit
from sklearn.preprocessing import LabelBinarizer
import numpy as np
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import pandas as pd
import sys
import time
import matplotlib.pyplot as plt

class Classfication:
    def __init__(self, path1, path2,path3):
        self.train = pd.read_csv(path1, encoding="gbk", index_col=0)
        self.test = pd.read_csv(path2, encoding="gbk", index_col=0)
        # self.all = pd.read_csv(path3, encoding="gbk", index_col=0)

    # 利用iris数据集划分训练数据和测试数据，最后得到的结果显示为图表
    def testTable(self):
        # 得到所有的列标签
        features = self.train.columns[:11]
        y = self.train['target'].values.tolist()
        clf = RandomForestClassifier(n_estimators=500, n_jobs=-1, oob_score=True, max_features="sqrt")
        # 放入训练的属性以及分类的特征值
        clf.fit(self.train[features], y)
        print features
        import_rate = clf.feature_importances_
        print clf.oob_score_
        # 初始化属性字典
        f_dict = {}
        # 将属性名和重要程度数值联系在一起
        for i in range(len(features)):
            f_dict[features[i]] = import_rate[i]
        # 重要程度按从大到小排序
        import_sort = sorted(f_dict.items(), key=lambda l: l[1], reverse=True)
        attr = []
        # 将属性名取出来
        for item in import_sort:
            attr.append(item[0])
        # 画图并保存
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
        # plt.figure()
        # plt.bar(range(len(import_rate)), import_rate, 0.2, tick_label=features)
        # plt.title(u"特征重要性系数")
        # # 绘制网格，网格为虚线
        # plt.grid(linestyle='--')
        # # X轴名称垂直化
        # plt.xticks(rotation=45)
        # plt.show()
        # plt.savefig("import-rate.png")
        return attr, features, y, clf


    def importAttr(self):
        attr, features, y, clf = self.testTable()
        # 选择最佳属性
        max_rate = 0
        befit_attr = []
        # 设置迭代次数
        iteration = 3
        all_rate = []
        for n in range(1, len(attr)+1):
            current_rate = 0
            for r in range(iteration):
                features = attr[:n]
                clf.fit(self.train[features], y)
                current_rate += clf.oob_score_
            current_rate = current_rate/iteration
            if current_rate > max_rate:
                max_rate = current_rate
                befit_attr = features
            all_rate.append(current_rate)
            print current_rate
        # 画图并保存
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
        plt.figure()
        plt.title(u'最佳特征个数选择')
        plt.xlabel(u'特征个数')
        plt.ylabel(u'oob-error')
        plt.plot(range(1, len(all_rate)+1), all_rate)
        plt.xticks(rotation=0)
        plt.grid(linestyle='--')
        plt.show()
        plt.savefig("attr-num.png")
        words = ''
        for word in befit_attr:
            words = words + ' ' + word
        print u'选择属性' + words + u'时最佳，oob误分率为' + str(max_rate)
        clf.fit(self.train[befit_attr], y)
        print clf.oob_score_
        result = clf.predict(self.test[befit_attr])
        print result

            # 预测训练集预测的类别，获得类别对应的名称
        # preds = clf.predict(self.test[features])
        # 第一个参数是行索引，第二个属性为列索引
        # print pd.crosstab(self.test['target'], preds, rownames=['actual'], colnames=['preds'])

        # 三种方法比较
    def compTest(self):
        # 生成用于聚类的各向同性高斯blob
        # n_samples: 待生成的样本的总数  n_features:每个样本的特征数
        # centers:要生成的样本中心（类别）数，或者是确定的中心点
        # random_state:random_state是随机数生成器使用的种子
        features = self.train.columns[:11]
        y = self.train['target'].values.tolist()
        X = self.train[features]
        y1, y2, y3, y4 = [], [], [], []
        for n in range(2,11):
            # 决策树分类器
            clf = DecisionTreeClassifier(min_samples_split=2)
            scores = cross_val_score(clf, X, y, cv=n)
            y1.append(scores.mean())
            # 随机森林分类器
            clf = RandomForestClassifier(n_estimators=500, min_samples_split=2, max_features="sqrt")
            scores = cross_val_score(clf, X, y, cv=n)
            y2.append(scores.mean())
            # 贝叶斯分类器
            clf = GaussianNB()
            scores = cross_val_score(clf, X, y, cv=n)
            y3.append(scores.mean())
            # SVM分类器
            clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
            scores = cross_val_score(clf, X, y, cv=n)
            y4.append(scores.mean())
            print u'正在进行'+str(n)+u'折验证'
            print y4
        # 画图对比
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
        plt.figure()
        X = range(2, 11)
        plt.title(u'算法比较')
        plt.xlabel('k')
        plt.ylabel(u'交叉验证')
        plt.plot(X, y1, label=u'决策树')
        plt.plot(X, y2, label=u'随机森林')
        plt.plot(X, y3, label=u'贝叶斯')
        plt.plot(X, y4, label=u'SVM')
        plt.xticks(rotation=0)  # X轴与名称相对应，名字不进行旋转
        plt.legend(bbox_to_anchor=[0.7, 0.3])  # 显示label名字
        plt.grid(linestyle='--')  # 画虚线网格
        plt.show()
        plt.savefig("compare.png")

# 设置编码
reload(sys)
sys.setdefaultencoding('utf-8')
start =time.clock()
path1 = 'train_data.csv'
path2 = 'test_data.csv'
path3 = 'data.csv'
cf = Classfication(path1, path2, path3)
# cf.testTable()
# cf.importAttr()
cf.compTest()
end = time.clock()
print u"任务已完成"
print u"完成时长：" + str(end-start)
