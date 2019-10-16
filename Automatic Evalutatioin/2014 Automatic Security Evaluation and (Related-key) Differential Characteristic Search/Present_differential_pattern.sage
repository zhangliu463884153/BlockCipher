# -*- coding: utf-8 -*-

sbox=[12,5,6,11,9,0,10,13,3,14,15,8,4,7,1,2]
from sage.crypto.sbox import SBox
S=SBox(sbox)
DDT=S.difference_distribution_table()
differential_pattern=[]
row=0
for x in DDT:
    for col in range(len(DDT[0])):
        if DDT[row][col]!=0:
            i= list(str('{0:b}'.format(row)).rjust(4,'0'))#将整数转为0,1二进制
            j= list(str('{0:b}'.format(col)).rjust(4,'0'))
            i=[int(k) for k in i]#将字符0,1转为int
            j=[int(k) for k in j]
            differential_pattern.append(i+j)
    row=row+1
    