scoreNum = 9
if scoreNum > 5:
    print("good")
else:
    print("bad")

# age = int(input('please enter your age'))
# if age < 3:
#     print('baby')

# elif age < 14:
#     print('teenage')
# else:
#     print('young')

eatlist = ['one', 'two', 'three', 'four']
for eat in eatlist:
    print(eat)

gafataDict = {'腾讯': 'Tencent', '阿里': 'Alibaba', '小米': 'xiaomi'}
for key, value in gafataDict.items():
    if (key == '阿里'):
        continue
    print(value.upper())
