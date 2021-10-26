from collections import OrderedDict
from typing import Dict
names = ['ahmed', 'hom', 'hamo', 'hhh', 'asmaa', 'amira', 'eman', 'saly', 'soso']
thedict = dict()
for i in names:
    if i[0] in thedict:
        thedict[i[0]].append(i)
    else:
        thedict[i[0]] = [i]


temp = sorted(thedict)
new = OrderedDict.fromkeys(temp, [])
for letter in temp:
    new[letter] = thedict[letter]

x= 5
print(x**2 + 3*x - 2)