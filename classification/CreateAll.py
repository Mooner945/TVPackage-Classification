#-*- coding:utf-8 -*-
# 创建所有用户需要用到的数据表格

import sys
import time
import pandas as pd

class CreateAll:
    def __init__(self, path1, path2, path3, path4, path5, path6):
        # 打开excel
        self.moneyD = pd.read_excel(path1)
        self.timeD = pd.read_excel(path2)
        self.liveP = pd.read_excel(path3)
        self.backP = pd.read_excel(path4)
        self.userInfo = pd.read_excel(path5)
        self.rate = pd.read_csv(path6, encoding="gbk")
        # 直播和回看信息一起计算所有频道的喜爱度
        self.allP = self.liveP.append(self.backP, ignore_index=True)
        self.target_set = {}
        self.t_n = 1
        # 获得所有的用户集合
        self.all_user = sorted(list(set(self.allP[u'设备号'])))
        self.money_user = sorted(list(set(self.moneyD[u'设备号'])))
        self.time_user = sorted(list(set(self.timeD[u'设备号'])))
        self.back_user = sorted(list(set(self.backP[u'设备号'])))
        self.live_user = sorted(list(set(self.liveP[u'设备号'])))
        self.user_set = sorted(list(set(self.rate[u'设备号'])))

    # 计算当前用户最喜欢的频道
    def computeP(self, user):
        if user in self.all_user:
            ui = self.allP[self.allP[u'设备号']==user]
            pro_set = set(ui[u'频道号'])
            # ui观看总次数
            Ci = len(ui)
            # ui观看频道数
            Ni =len(pro_set)
            # ui观看所有频道总时长
            sum_timei = ui[u'观看时间'].sum()
            # 创建用户频道喜爱度字典
            pro_dict = {}
            for pro in pro_set:
                vj = self.allP[self.allP[u'频道号']==pro]
                ij = ui[ui[u'频道号']==pro]
                user_set = set(vj[u'设备号'])
                # vj被用户观看总次数
                Cj = len(vj)
                # 观看vj的用户数
                Mj = len(user_set)
                # ui观看vj总次数
                Cij = float(len(ij))
                # vj被全体用户观看的总时长
                sum_timej = vj[u'观看时间'].sum()
                # ui观看vj的总时长
                sum_timeij = float(ij[u'观看时间'].sum())
                # 计算偏好
                a = sum_timeij/(sum_timej/Mj)
                b = Cij/(Ci/Ni)
                c = sum_timeij/(sum_timei/Ni)
                d = Cij/(Ci/Ni)
                Rij = a*b*c*d
                # 保留前2位
                Rij = float('%.4f' % Rij)
                pro_dict[pro] = Rij
            pro_sort = sorted(pro_dict.items(), key=lambda l: l[1], reverse=True)
            # 最喜欢的频道列表
            like_pros = pro_sort[0:1]
            like_pro = like_pros[0][0]
        else:
            like_pro = 0
        # 返回用户最喜欢的频道号
        return like_pro

    # 计算用户最喜欢观看电视的时间段
    def watchTime(self, user):
        if user in self.all_user:
            ui = self.allP[self.allP[u'设备号'] == user]
            # 初始化时间段字典
            time_dict = {u'凌晨': 0, u'上午': 0, u'下午': 0, u'晚上': 0}
            for i in ui.index:
                start = ui.loc[i, u'开始时间']
                end = ui.loc[i, u'结束时间']
                date = ui.loc[i, u'统计时间']
                day = str(date)
                min_time = pd.Timestamp(day)
                # 如果观看时间不是深夜到凌晨，即不跨夜
                if min_time <= start:
                    a = min_time
                    b = pd.Timestamp(day + ' 6:00')
                    c = pd.Timestamp(day + ' 12:00')
                    d = pd.Timestamp(day + ' 18:00')
                    if date == 20170731:
                        day = str(20170801)
                    elif date == 20170831:
                        day = str(20170901)
                    elif date == 20170930:
                        day = str(20171001)
                    else:
                        day = str(date+1)
                    e = pd.Timestamp(day)
                    time_list = [a, b, c, d, e]
                    time_name = [u'凌晨', u'上午', u'下午', u'晚上']
                    for t in range(len(time_list)-1):
                        if start >= time_list[t] and start <= time_list[t+1]:
                            if end < time_list[t+1]:
                                time_dict[time_name[t]] += (end - start).seconds / 60
                            elif end >= time_list[t+1] and end < time_list[t+2]:
                                time_dict[time_name[t]] += (time_list[t+1] - start).seconds / 60
                                time_dict[time_name[t+1]] += (end - time_list[t+1]).seconds / 60
                # 如果跨夜了，由于筛选的时间为6小时以内，故只有一种可能
                else:
                    h = pd.Timestamp(day)
                    time_dict[u'晚上'] += (h - start).seconds / 60
                    time_dict[u'凌晨'] += (end - h).seconds / 60
            time_sort = sorted(time_dict.items(), key=lambda l: l[1], reverse=True)
            # print time_sort
            # 最喜欢的观看时间列表
            like_times = time_sort[0:1]
            like_time = like_times[0][0]
            ti = {u'凌晨': 1, u'上午': 2, u'下午': 3, u'晚上': 4}
            time_id = ti[like_time]
        else:
            like_time = 'none'
            time_id = 0
        return time_id, like_time

    # 计算直播次数以及观看直播天数
    def countLive(self, user):
        if user in self.live_user:
            ui = self.liveP[self.liveP[u'设备号'] == user]
            data_num = len(ui)
            date_set = set(ui[u'统计时间'])
            day_num = len(date_set)
        else:
            data_num = 0
            day_num = 0
        return data_num, day_num

    # 计算回看次数以及回看频道数
    def countBack(self, user):
        if user in self.back_user:
            ui = self.backP[self.backP[u'设备号'] == user]
            data_num = len(ui)
            date_set = set(ui[u'统计时间'])
            day_num = len(date_set)
        else:
            data_num = 0
            day_num = 0
        return data_num, day_num

    # 计算点播次数以及点播节目数
    def countMoney(self, user):
        if user in self.money_user:
            ui = self.moneyD[self.moneyD[u'设备号'] == user]
            data_num = len(ui)
            # 观看每个节目的金额
            pro_money = ui[u'点播金额']
            m = pro_money.mean()
            m = float('%.2f' % m)
            date_set = set(ui[u'点播日期'])
            day_num = len(date_set)
        else:
            data_num = 0
            day_num = 0
            m = 0.0
        # print data_num, pro_num, m
        return data_num, day_num

    # 计算单片点播次数以及点播节目数
    def countTime(self, user):
        if user in self.time_user:
            ui = self.timeD[self.timeD[u'设备号'] == user]
            data_num = len(ui)
            # 观看每个节目的时间
            pro_time = ui[u'观看时间']
            t = pro_time.mean()
            t = float('%.2f' % t)
            date_set = set(ui[u'点播日期'])
            day_num = len(date_set)
        else:
            data_num = 0
            day_num = 0
            t = 0.0
        # print data_num, pro_num, t
        return data_num, day_num

    # 获取用户套餐并将套餐数字化
    def getTarget(self, user):
        ui = self.userInfo[self.userInfo[u'设备号'] == user]
        target_name = list(ui[u'套餐'])
        target_name = target_name[0]
        target = 0
        # if target_name == u'普通套餐':
        #     target = 0
        # elif target_name == u'乐惠套餐':
        #     target = 1
        # elif target_name == u'月享套餐':
        #     target = 2
        # elif u'融合套餐' in target_name:
        #     target = 3
        target = 0
        if target_name in self.target_set:
            target = self.target_set[target_name]
        elif target_name != u"普通套餐":
            target = self.t_n
            self.target_set[target_name] = self.t_n
            self.t_n += 1
        else:
            target = 0
        return target, target_name

    # 处理评分信息，得到用户最喜爱类型
    def dealScore(self, user):
        if user in self.user_set:
            ui = self.rate[self.rate[u'设备号'] == user]
            types = {}
            # 筛选最喜爱的类型，将每个类型赋值权重相加
            for i in ui.index:
                t = ui.loc[i, u'类型']
                r = ui.loc[i, u'喜爱度']
                words = t.strip().split('/')
                for word in words:
                    word = word.strip()
                    if word in types:
                        types[word] += r
                    else:
                        types[word] = r
            types_sort = sorted(types.items(), key=lambda l: l[1], reverse=True)
            # 最喜欢的类型列表
            like_types = types_sort[0:1]
            like_type = like_types[0][0]
        else:
            like_type = u"无"
        return like_type

    # 主程序，进行循环
    def saveInfo(self):
        # 初始化信息列表
        L = []
        type_set = {}
        # 初始化类别ID
        n = 1
        for user in self.user_set:
            like_pro = self.computeP(user)
            time_id, like_time = self.watchTime(user)
            live_data, live_day = self.countLive(user)
            back_data, back_day = self.countBack(user)
            money_data, money_day = self.countMoney(user)
            time_data, time_day = self.countTime(user)
            target, target_name = self.getTarget(user)
            like_type = self.dealScore(user)
            type_id = 0
            if like_type in type_set:
                type_id = type_set[like_type]
            elif like_type != u"无":
                type_id = n
                type_set[like_type] = n
                n += 1
            else:
                type_id = 0
            new = [user, like_pro, time_id, type_id, live_data, live_day, back_data, back_day, money_data,
                   money_day, time_data, time_day, target, target_name, like_time, like_type]
            L.append(new)
            print u"正在处理设备号为" + str(user) + u"的用户"
        rec = pd.DataFrame(L, columns=[u'设备号', u'喜爱频道', u'时间段', u'类型id', u'直播次数',u'直播天数',
                                       u'回看次数', u'回看天数', u'点播次数', u'点播天数',
                                       u'单片点播次数', u'单片点播天数',
                                       u'target', u'target_name', u'观看时间段', u'喜爱类型'])
        rec.to_csv("data.csv", encoding="gbk", index=False)


path1 = u'F:\\postgraduate\\期刊论文\\用户点播.xlsx'
path2 = u'F:\\postgraduate\\期刊论文\\用户单片点播.xlsx'
path3 = u'F:\\postgraduate\\期刊论文\\用户直播.xlsx'
path4 = u'F:\\postgraduate\\期刊论文\\用户回看.xlsx'
path5 = u'F:\\postgraduate\\期刊论文\\用户信息.xlsx'
path6 = 'F:\\python-save\\myPaper\\model\\train_score.csv'
# 设置编码
reload(sys)
sys.setdefaultencoding('utf-8')
start =time.clock()
ca = CreateAll(path1, path2, path3, path4, path5, path6)
ca.saveInfo()
end = time.clock()
print u"任务已完成"
print u"完成时长：" + str(end-start)