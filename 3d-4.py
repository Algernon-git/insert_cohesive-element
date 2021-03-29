max_node_len=5
ori_inp=open("Job-dengzhilong.inp",'r')
Inp_line=ori_inp.readlines()
value=0
k=0
Node_dic={}
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Node'):
        value+=1
    if Inp_line[i].startswith('*Element'):
        value=0
        break
    if value==1:
        k+=1
        if k>1:
            L=Inp_line[i].replace(' ','').replace('\n','').split(',')
            Node_dic[L[0]]=L[1:]
    else:
        pass
max_node=k-1
print(max_node)
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Elset, elset=Set-1, generate'):
        Unfracture_start=int(Inp_line[i+1].replace(' ','').replace('\n','').split(',')[0])
        Unfracture_end=int(Inp_line[i+1].replace(' ','').replace('\n','').split(',')[1])
    elif Inp_line[i].startswith('*Elset, elset=Set-2, generate'):
        Fracture_start=int(Inp_line[i+1].replace(' ','').replace('\n','').split(',')[0])
        Fracture_end=int(Inp_line[i+1].replace(' ','').replace('\n','').split(',')[1])
print(Unfracture_start,Unfracture_end)
print(Fracture_start,Fracture_end)
value=0
k=0
Unfracture_dic={}
Fracture_dic={}
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Element'):
        value+=1
    if Inp_line[i].startswith('*Elset'):
        value=0
        break
    if value==1:
        k+=1
        if k>1:
            ele=Inp_line[i].replace(' ','').replace('\n','').split(',')
            if int(ele[0]) in range(Unfracture_start,Unfracture_end+1):
                Unfracture_dic[ele[0]]=ele[1:5]
            elif int(ele[0]) in range(Fracture_start,Fracture_end+1):
                Fracture_dic[ele[0]]=ele[1:5]
    else:
        pass
Node_fracture_lis=[]
Node_unfracture_lis=[]
Node_edge_lis=[]
for i in Unfracture_dic:
    for j in Unfracture_dic[i]:
        if j not in Node_unfracture_lis:
            Node_unfracture_lis.append(j)
for i in Fracture_dic:
    for j in Fracture_dic[i]:
        if j not in Node_fracture_lis:
            Node_fracture_lis.append(j)
        if j in Node_unfracture_lis and j not in Node_edge_lis:
                Node_edge_lis.append(j)
 
Node_appeartimes=dict.fromkeys(Node_fracture_lis,0)
for i in Fracture_dic:
    for j in Fracture_dic[i]:
        if j in Node_fracture_lis:
            Node_appeartimes[j]+=1
New_node_dic={}
for i in Node_dic:
    if i not in Node_fracture_lis:
        New_node_dic[i]=Node_dic[i]
    if i in Node_fracture_lis:
        for j in range(Node_appeartimes[i]+1):
            New_node_dic[str(j*(10**(len(str(max_node))))+int(i))]=Node_dic[i]
New_node_assign=dict.fromkeys(New_node_dic,1)
New_node_dic_sort=sorted([int(i) for i in New_node_dic.keys()])
New_inp=open('New_inp.txt','w')
for i in range(len(Inp_line)):
    New_inp.write(Inp_line[i])
    if Inp_line[i].startswith('*Node'):
        break
for i in New_node_dic_sort:
    New_inp.write(str(i))
    New_inp.write(', ')
    New_inp.write(New_node_dic[str(i)][0])
    New_inp.write(', ')
    New_inp.write(New_node_dic[str(i)][1])
    New_inp.write(', ')
    New_inp.write(New_node_dic[str(i)][2])
    New_inp.write('\n')
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Element'):
        for j in range(Unfracture_end+1):
            New_inp.write(Inp_line[i+j])
        break
for i in Node_unfracture_lis:
    New_node_assign[i]=0
def yu(x):
    if len(x)<=max_node_len:
        return x
    if len(x)>max_node_len:
        return str(int(x[-max_node_len:]))
for i in Fracture_dic:
    for j in range(4):
        for k in New_node_assign:
            if New_node_assign[k]!=0 and yu(k)==Fracture_dic[i][j]:
                Fracture_dic[i][j]=k
                New_node_assign[k]=0                
for i in range(len(Inp_line)):
    if Inp_line[i].startswith(str(Fracture_start)):
        for j in range(Fracture_end-Fracture_start+1):
            New_inp.write(str(Fracture_start+j))
            New_inp.write(', ')
            New_inp.write(Fracture_dic[str(Fracture_start+j)][0])
            New_inp.write(', ')
            New_inp.write(Fracture_dic[str(Fracture_start+j)][1])
            New_inp.write(', ')
            New_inp.write(Fracture_dic[str(Fracture_start+j)][2])
            New_inp.write(', ')
            New_inp.write(Fracture_dic[str(Fracture_start+j)][3])
            l=0
            for k in Inp_line[i+j]:
                if k==',':
                    l+=1
                if l>=5:
                    New_inp.write(k)
        break
#开始生成cohesive单元
New_inp.write('*Element, type=COH3D6\n')
Cohesive_dic={}
k=Fracture_end+1
for i in Fracture_dic:
    for j in Unfracture_dic:
        l=[]
        for m in Fracture_dic[i]:
            if yu(m) in Unfracture_dic[j]:
                l.append([m,yu(m)])
        if len(l)==3:
            Cohesive_dic[str(k)]=[l[0][0],l[1][0],l[2][0],l[0][1],l[1][1],l[2][1]]
            k+=1
k1=k
Fracture_dic_sort=sorted([int(i) for i in Fracture_dic.keys()])
for i in Fracture_dic_sort:
    for j in range(i+1,Fracture_end+1):
        l=[]
        for m in Fracture_dic[str(i)]:
            for n in Fracture_dic[str(j)]:
                if yu(m)==yu(n):
                    l.append([m,n])
        if len(l)==3:
            Cohesive_dic[str(k)]=[l[0][0],l[1][0],l[2][0],l[0][1],l[1][1],l[2][1]]
            k+=1
k2=k
for i in range(Fracture_end+1,k2):
    New_inp.write(str(i))
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][0])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][1])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][2])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][3])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][4])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][5])
    New_inp.write('\n')
                  
New_inp.close()
print(k1)
print(k2)

        
        
        


            
        
    

               

