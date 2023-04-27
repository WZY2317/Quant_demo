import talib

foodlist = ['apple', 'pear', 'orange']  # 注释
foodlist.append('noodles')
numlist = [1, 2, 5, 8, 4, 7, 0]
numlist.sort(reverse=True)
print(numlist)

#print(foodlist)

# foodlist[-1]
# print(foodlist[-1])
# Len = len(foodlist)
# foodlist.append('banana')
# print(foodlist[0:2])
# theCoinTrade = set()
# theCoinTrade.update(['币安', '欧易', '火币'])
# print(theCoinTrade)
# theCoinTrade.discard('火币')
# print(theCoinTrade)
StuNum = {'tom': '1', 'jerry': '2', 'rose': '3', 'jack': '4'}
StuNum['amy'] = 1
StuNum['tom'] = 10
del StuNum['amy']

print(StuNum)


def IsWeekend(day: int) -> bool:
    if day == 6 or day == 7:
        print("weekend")
    else:
        print('week day')


flag = IsWeekend(5)
# print(StuNum)
# StuNum['wang'] = '5'
# print(StuNum)
# del StuNum['jack']
# print(StuNum)

# def sma(self, n, array=False):
#     """简单均线"""
#     result = talib.SMA(self.close, n)
#     if (array):
#         return result
#     else:
#         return result[-1]

# CV = None

# sum = lambda arg1, arg2: arg1 + arg2

# # 调用sum函数
# print("相加后的值为 : ", sum(10, 20))

sum = 9


def func(parmer1, parmer2) -> int:
    parmer1 += 2
    parmer2 += 2
    s = 0.9
    return s


p1, p2 = func(2, 3)

sum = lambda p1, p2: p1 + p2

sum(1, 5)

# p1, p2 = func(2, 3)
# print(p1, p2)

# def IsGrown(age):
#     if (age := 18) > 18:
#         print("成年")
#     else:
#         print("未成年")