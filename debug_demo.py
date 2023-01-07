import datetime


def sum_even(n):
    sum = 0
    for i in range(0, n, 2):
        # assert (i % 2 == 1)
        # print(i)
        sum += i
    return sum


# sum(50)
n = sum_even(50)
print(n)
print("time now:", datetime.datetime.now())
