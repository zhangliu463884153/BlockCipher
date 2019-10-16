# -*- coding: utf-8 -*-

#PRESENT-80
#sbox=[12,5,6,11,9,0,10,13,3,14,15,8,4,7,1,2]

DDT=[[0,0],
      [1,3],[1,7],[1,9],[1,13],
      [2,3],[2,5],[2,6],[2,10],[2,12],[2,13],[2,14],
      [3,1],[3,3],[3,4],[3,6],[3,7],[3,10],[3,11],
      [4,5],[4,6],[4,7],[4,9],[4,10],[4,12],[4,14],
      [5,1],[5,4],[5,9],[5,10],[5,11],[5,12],[5,13],
      [6,2],[6,6],[6,8],[6,11],[6,12],[6,15],
      [7,1],[7,2],[7,6],[7,8],[7,12],[7,15],
      [8,3],[8,7],[8,9],[8,11],[8,13],[8,15],
      [9,2],[9,4],[9,6],[9,8],[9,12],[9,14],
      [10,2],[10,3],[10,5],[10,8],[10,10],[10,13],[10,14],
      [11,1],[11,4],[11,8],[11,9],[11,10],[11,11],[11,13],
      [12,2],[12,5],[12,7],[12,8],[12,9],[12,10],[12,14],
      [13,1],[13,2],[13,3],[13,4],[13,7],[13,10],[13,11],
      [14,2],[14,3],[14,6],[14,7],[14,8],[14,9],[14,12],[14,13],
      [15,1],[15,4],[15,14],[14,15]]


vertexs=[]
for i in range(len(DDT)):
    
    input_differential=list(str('{0:b}'.format(DDT[i][0])).rjust(4,'0'))
    output_differential=list(str('{0:b}'.format(DDT[i][1])).rjust(4,'0'))
    total=input_differential+output_differential
    total=[int(x) for x in total]
    vertexs.append(total)
    
filename="H_reprensentation_of_convex_hull.txt"
f=open(filename,'w')
Hull=Polyhedron(vertexs)
H_representation=[]
for v in Hull.inequalities_list():
    H_representation.append(v)
    
for i in H_representation: 
    f.writelines(str(i)+"\n")
    
f.close()