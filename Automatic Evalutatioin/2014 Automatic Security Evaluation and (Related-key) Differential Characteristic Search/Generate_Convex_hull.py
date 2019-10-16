# -*- coding: utf-8 -*-
import copy
def choose(x,y):#使用贪婪算法从凸包中选取不等式进行剔除
    
    N1=len(x)
    N2=len(y)
    z=[0]*N1
    #How many points are not satisfed for each inequality.
	#不满足的点越多，产生的约束越强。
    for i in range(N1):
        for j in range(N2):
            if x[i][0]*y[j][0]+x[i][1]*y[j][1]+x[i][2]*y[j][2]+x[i][3]*y[j][3]+x[i][4]*y[j][4]+x[i][5]*y[j][5]+ \
            x[i][6]*y[j][6]+x[i][7]*y[j][7]+x[i][8]<0:
                z[i]=z[i]+1
    temp=z[0]
    j=0
    #Finding the inequality and its count is the largest.
    for i in range(1,N1):
        if z[i]>temp:
            j=i
            temp=z[j]
            
    if temp!=0:
        for i in range(N2):
            if x[j][0]*y[i][0]+x[j][1]*y[i][1]+x[j][2]*y[i][2]+x[j][3]*y[i][3]+\
            x[j][4]*y[i][4]+x[j][5]*y[i][5]+x[j][6]*y[i][6]+x[j][7]*y[i][7]+x[j][8]<0:
                y[i][0]=0;y[i][1]=0;y[i][2]=0;y[i][3]=0;y[i][4]=0;y[i][5]=0;y[i][6]=0;y[i][7]=0; 
    
        #Output inequality and the number of points that are not satisfed.
        '''
        fp=open(filename,'w')
        for i in range(8):
            if x[j][i]<0 or i==0:
                fp.write(str(x[j][i])+"*x"+str(i+1))
            else:
                fp.write("+"+str(x[j][i])+"*x"+str(i+1))
                
        fp.write(" >= "+str(x[j][8])+"*x"+str(temp)+"\n")
        '''
        c=copy.copy(x[j])#直接将x[j]使用append添加，添加进去的都是0
        
        #select_convex_hull.append([c,temp])
        select_convex_hull.append(c)
        
        x[j][0]=0;x[j][1]=0;x[j][2]=0;x[j][3]=0;x[j][4]=0;x[j][5]=0;x[j][6]=0;x[j][7]=0;x[j][8]=0;
        
        return temp
    else:
        return 0

def ddt_ten_to_two(Differential_Distribution_Table):#将十进制差分分布表转换为二进制，方便生成凸包不等式
    vertexs=[]
    for i in range(len(Differential_Distribution_Table)):
        
        input_differential=list(str('{0:b}'.format(Differential_Distribution_Table[i][0])).rjust(4,'0'))
        output_differential=list(str('{0:b}'.format(Differential_Distribution_Table[i][1])).rjust(4,'0'))
        total=input_differential+output_differential
        total=[int(x) for x in total]
        vertexs.append(total)
    return vertexs


sbox=[]
with open('Present_sbox.txt', 'r') as f:
#with open('sbox.txt', 'r') as f:
    for line in f:
        sbox.append(int(line))

from sage.crypto.sbox import SBox
S=SBox(sbox)
ddt=S.difference_distribution_table()

DDT=[]
no_exist_ddt=[]
for i in range(len(sbox)):
    for j in range(len(sbox)):
        if ddt[i][j]!=0:
            DDT.append([i,j])
        elif ddt[i][j]==0:
            no_exist_ddt.append([i,j])



vertexs=ddt_ten_to_two(DDT)#存在的差分路径
no_exit_differential=ddt_ten_to_two(no_exist_ddt)#不存在的差分路径


#filename="Present_ddt_convex_hull.txt"
filename="LBlock_S0_ddt_convex_hull.txt"
f=open(filename,'w')
Hull=Polyhedron(vertexs)
Inequality=[]#存储凸包不等式系数
for v in Hull.inequalities_list():
    v=v[1:]+ v[:1]#生成的列表需要调换一下位置。
    f.writelines(str(v)+"\n")
    Inequality.append(v)
f.close()


filename="select_convex_hull_inequality.txt"
fp=open(filename,'w')


global select_convex_hull
select_convex_hull=[]


while(choose(Inequality,no_exit_differential)!=0):
    choose(Inequality,no_exit_differential);

for i in select_convex_hull:
    fp.writelines(str(i)+"\n")
    
fp.close()