# 더하는 기능을 하는 함수 정의

def add(*num):
    """ num1 int, num2 int -> 더하는 기능"""
    total = 0
    for i in num:
        total += i
    return total    

# 빼기하는 기능을 하는 함수 정의

def sub(*num):
    """ num1 int, num2 int -> 빼는 기능"""
    total = 0
    for i in num:
        total -= i
    return total