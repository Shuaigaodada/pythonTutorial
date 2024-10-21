# 总分: 150, 及格80分, 50分为附加分(pro max)
"""
九九乘法表(15分)
问题: 
    输出九九乘法表，每输出完一行则换行。使用\t制表符隔开。
"""
for i in range(1, 10):
    for j in range(i, 10):
        print(f"{i}*{j}={i * j}", end="\t")
    print()

"""
总和是什么(5分)
问题: 
    计算1到12345678的和。
"""
sum = 0
for i in range(1, 12345678):
    sum += i
print(sum)
"""
5的倍数(10分)
问题: 
    输出1到100中所有5的倍数。
"""
num = 0
while num < 100:
    num += 5
    print(num)

"""
可被除整(40分)
问题:
    输出1到100中所有能被3整除的数。
"""
for i in range(1, 101):
    if i % 3 == 0:
        print(i)

"""
什么抽象平方根(20分)
问题:
    通过循环得出x的平方根，x的次方为整数。
"""
x = 1936
num = 2
while num ** 2 != x:
    num += 1
print(num)
"""
总和是什么 pro max(10分)
问题: 
    计算1到1234567890的和, 不使用循环。(提示: 使用数学公式)
"""
n = 1234567890
sum = n * (n + 1) // 2
print(sum)
"""
九九乘法表 pro max(25分)
问题: 
    输出九九乘法表，每行输出5个乘法表达式，中间通过制表符隔开，每输出5个表达式换行。

操作提示：
    print() - 函数可以输出一个空行。
    print有一个参数叫做end，可以指定输出的结尾，默认是换行符。
    print("mytext", end="\t") - 表示输出后不换行，而是输出一个制表符。
    print(f"{myvar}") - 可以输出变量myvar的值。
解题思路:
    1. 使用两个for循环，外层循环i从1到9，内层循环j从i到9。
    2. 输出乘法表达式i * j = i * j，中间通过制表符隔开。
    3. 使用lineCounter变量记录输出的表达式个数，每输出5个表达式换行。
侧重点:
    1. for循环的使用。
    2. 输出格式的控制。
    3. 条件判断的使用。
    4. %运算符的使用。
    5. counter变量的使用。
"""
lineCounter = 0
for i in range(1, 10):
    for j in range(i, 10):
        print(f"{i} * {j} = {i * j}", end="\t")
        lineCounter += 1
        if lineCounter % 5 == 0:
            print()

"""
可能性 pro max(25分)
问题:
    输出1, 2, 3, 4的所有排列组合(不重复)。
操作提示:
    and - 逻辑与运算符。
    or - 逻辑或运算符。
解题思路:
    1. 使用三个for循环，外层循环i从1到4，中间循环j从1到4，内层循环k从1到4。
    2. 使用if条件判断，判断i、j、k是否不相等。
    3. 输出i、j、k。
侧重点:
    1. for循环的使用。
    2. 条件判断的使用。
    3. 输出格式的控制。
    4. 逻辑运算符的使用。
    5. 循环嵌套的使用。
"""
for i in range(1, 5):
    for j in range(1, 5):
        for k in range(1, 5):
            if i != j and i != k and j != k:
                print(i, j, k)


