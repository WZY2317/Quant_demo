import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

examDict = {
    '学习时间': [
        0.5, 0.75, 1.00, 1.25, 1.50, 1.75, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00,
        3.25, 3.50, 4.00, 4.25, 4.50, 4.75, 5.00, 5.50
    ],
    '学习成绩': [
        10, 22, 13, 43, 20, 22, 33, 50, 62, 48, 55, 75, 62, 73, 81, 76, 64, 82,
        90, 93
    ]
}
examOrderDict = OrderedDict(examDict)
examDf = pd.DataFrame(examOrderDict)  #构建数据框
print(examDf.head())
exam_X = examDf.loc[:, '学习时间']
exam_y = examDf.loc[:, '学习成绩']
plt.scatter(exam_X, exam_y, color='b', label='exam_data')
plt.xlabel('Hours')
plt.ylabel('Grades')
plt.show()
#建立训练数据和测试数据
X_train, X_test, y_train, y_test = train_test_split(exam_X,
                                                    exam_y,
                                                    train_size=0.8)
print(exam_X.shape, '原始训练数据特征')
print(X_train.shape, "训练数据特征")
print(X_test.shape, "测试训练特征")

print(exam_y.shape, "原始训练数据特征")
print(y_train.shape, "训练数据特征")
print(y_test.shape, "测试训练特征")
plt.scatter(X_train, y_train, color='b', label='train_data')
plt.scatter(X_test, y_test, color='red', label='test_data')
plt.legend(loc=2)
plt.xlabel('Hours')
plt.ylabel('grades')
plt.show()
X_train = X_train.values.reshape(-1, 1)
y_train = y_train.values.reshape(-1, 1)
#第一步导入线性回归

#第二步创建模型,线性回归
model = LinearRegression()
#第三步训练模型
model.fit(X_train, y_train)

#建立最佳拟合线
a = model.intercept_
b = model.coef_
print('最佳拟合曲线,截距a=', a, '回归系数b=', b)
plt.scatter(X_train, y_train, color='b', label='tarin data')

y_train_pred = model.predict(X_train)
plt.plot(X_train,
         y_train_pred,
         color='black',
         linewidth='3',
         label='best line')
plt.legend(loc=2)
plt.xlabel('Hours')
plt.ylabel('grades')
plt.show()
rDf = examDf.corr()
print('相关系数矩阵')
rDf
X_test = X_test.values.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)
model.score(X_test, y_test)
print(model.score(X_test, y_test))