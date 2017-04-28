""" Generate input for project in format:
    [P pounds]
    [M dollars]
    [N number of items]
    [C number of constraints]
    [item_name]; [class]; [weight]; [cost]; [resale value]
    [item_name]; [class]; [weight]; [cost]; [resale value]
    ...
    [incompatible_class1, incompatible_class2, incompatible_class3]
    [incompatible_class4, incompatible_class5]
    ...
    [end of file]

    Domains:
        P < 2^32 .00
        M < 2^32 .00
        N <= 200,000 integer
        C <= 200,000 integer
        item name unique and alphanumeric (_)
        class [0, N-1]
        weight .00
        cost .00
        resale value .00
        incompatibility list <= 199,999
        file size < 4Mb
"""

from random import *

####

filename = 'problem1.in'
f = open(filename, "w")

P = 2**20
M = 2**20
N = 50000
C = 25000

f.write("%d\n" % P)
f.write("%d\n" % M)
f.write("%d\n" % N)
f.write("%d\n" % C)

basename = 'item_'

for i in range(N):
    weight = randint(100, 10000) / 100
    x = randint(100, 10000) / 100
    y = randint(100, 10000) / 100

    cost = min(x, y)
    resale = max(x, y)

    line = "; ".join([basename + str(i), str(i), str(weight), str(cost), str(resale)])
    line += "\n"
    f.write(line)

for i in range(C):
    num = randint(2,4)
    S = set([])
    while len(S) < num:
        x = randint(0, N - 1)
        S.add(str(x))
    L = list(S)
    line = ", ".join(L)
    line += "\n"
    f.write(line)

f.close()

####

filename = 'problem2.in'
f = open(filename, "w")

P = 2**25
M = 2**20
N = 20000
C = 100000

f.write("%d\n" % P)
f.write("%d\n" % M)
f.write("%d\n" % N)
f.write("%d\n" % C)

basename = 'item_'

for i in range(N):
    weight = randint(100, 1000000) / 100
    x = randint(100, 80000) / 100
    y = randint(100, 80000) / 100

    cost = min(x, y)
    resale = max(x, y)

    line = "; ".join([basename + str(i), str(i), str(weight), str(cost), str(resale)])
    line += "\n"
    f.write(line)

for i in range(C):
    num = randint(2,5)
    S = set([])
    while len(S) < num:
        x = randint(0, N - 1)
        S.add(str(x))
    L = list(S)
    line = ", ".join(L)
    line += "\n"
    f.write(line)

f.close()

####

filename = 'problem3.in'
f = open(filename, "w")

P = 2**20
M = 2**25
N = 50000
C = 70000

f.write("%d\n" % P)
f.write("%d\n" % M)
f.write("%d\n" % N)
f.write("%d\n" % C)

basename = 'item_'

for i in range(N):
    weight = randint(100, 20000) / 100
    x = randint(100, 200000) / 100
    y = randint(100, 200000) / 100

    cost = min(x, y)
    resale = max(x, y)

    line = "; ".join([basename + str(i), str(i), str(weight), str(cost), str(resale)])
    line += "\n"
    f.write(line)

for i in range(C):
    num = randint(2,6)
    S = set([])
    while len(S) < num:
        x = randint(0, N - 1)
        S.add(str(x))
    L = list(S)
    line = ", ".join(L)
    line += "\n"
    f.write(line)

f.close()