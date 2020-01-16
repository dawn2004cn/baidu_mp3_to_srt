import pandas

from pandas.plotting import scatter_matrix

import matplotlib.pylab as plt

import matplotlib
import sys

from sklearn import model_selection

from sklearn.metrics import  classification

from sklearn.metrics import classification_report

from sklearn.metrics import confusion_matrix

from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.neighbors import KNeighborsClassifier

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.naive_bayes import GaussianNB

from sklearn.svm import SVC

print(matplotlib.__file__)

print(matplotlib.get_cachedir())

#加载鸢尾花的数据集合

iris_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

iris_attrs=['花萼长度','花萼宽度','花瓣长度','花瓣宽度','种类']

#注意：这里的参数names需要进行指定，否则或出现数据类型不匹配

iris_dataset=pandas.read_csv(iris_url,names=iris_attrs)

print(iris_dataset.head(10))

#自定义字体,解决中文显示问题

plt.rcParams['font.family'] = ['Microsoft YaHei']

plt.rcParams['axes.unicode_minus'] = False

#单变量绘图

#iris_dataset.plot(kind='box', subplots=True,layout=(2,2),sharex=False,sharey=False);

#柱状图显示

#iris_dataset.hist()

#属性两两对比散点图

#scatter_matrix(iris_dataset)

#数据集分割： 80%作为训练集 20%作为验证集

dataset_array = iris_dataset.values

X = dataset_array[:,0:4]

Y = dataset_array[:,4]

validation_ration = 0.2

rand_seed  = 7

#X_train Y_train 训练集   X_validataion Y_validataion 验证集,

X_train,X_validation,Y_train,Y_validation = model_selection.train_test_split(X,Y,test_size=validation_ration,random_state=rand_seed)

#测试工具集，使用十折交叉验证来估计算法准确率

scoring = 'accuracy'

#建立模型：通过评估不同的算法，建立模型

iris_models = []

#逻辑回归算法

iris_models.append(('LR',LogisticRegression()))

#线性判别分析法

iris_models.append(('LDA',LinearDiscriminantAnalysis()))

#K近邻法

iris_models.append(('KNN',KNeighborsClassifier()))

#分类回归数/决策树

iris_models.append(('CART',DecisionTreeClassifier()))

#高斯朴素贝叶斯分类器

iris_models.append(('NB',GaussianNB()))

#支持向量机

iris_models.append(('SVM',SVC()))

#验证每一个模型

results=[]

names = []

for name,model in iris_models:

   kfold = model_selection.KFold(n_splits=10,random_state=rand_seed)

   cv_results = model_selection.cross_val_score(model,X_train,Y_train,cv=kfold,scoring=scoring)

   results.append(cv_results)

   names.append(name)

   result_msg = "模型%s: 均值%f (均方差%f)" % (name,cv_results.mean(),cv_results.std())

   print(result_msg)

#绘制模型评估结果

figure = plt.figure()

figure.suptitle("算法验证比对")

ax = figure.add_subplot(111)

plt.boxplot(results)

ax.set_xticklabels(names)
plt.show()