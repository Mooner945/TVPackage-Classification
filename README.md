# 电视增值套餐分类
### 执行程序顺序：
* preTreatment（预处理）：
  * （首页带有"用户……"的excel文件是已经经过预处理的，若要进行预处理，需要使用原始数据）
  * 1.reName.py:将excel中的电视节目提取关键字并重命名
  * 2.Spider.py:从豆瓣爬取相应节目的信息
  * 3.supplement.py:有些数据没有爬下来或者出错了，需要手动纠错，通过此程序手动补充
* model（模型）：
  * （model里面的csv文件是已经处理过的文件）
  * 1.DivisionTest.py:使用哪些数据，这里使用所有数据
  * 2.improCompScore.py:改进的模型，用于训练（只用使用一个模型）
* classification（分类训练）：
  * 1.CreateAll.py:创建训练数据
  * 2.Division.py:划分用于训练的用户与需要套餐推送的用户
  * 3.Classfication.py:利用随机森林进行训练
