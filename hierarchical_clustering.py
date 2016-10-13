# -*- coding: Latin-1 -*-
import itertools
from itertools import chain
from itertools import groupby
import sys
import math
import heapq
import csv
import numpy

def execute(inp,k):   
    euc_distance=[]
    a=[]
    combi = []
    data1=[]
    heap=[]
    cluster = []
    cen=[]
    c=[]
    elem1=[]
    data=[]
    
    with open(inp,'rb') as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        first_row = next(reader)
        num_col = len(first_row)

    with open(inp, 'rb') as f:
        dat = [(line.rstrip('\n').split(',')[0:num_col-1]) for line in f.readlines()]

    for i in dat:
        data.append(map(float, i))
    for i in range(len(data)):
        data1.append(list((data[i],i)))
        cluster.append([i])
    def distance(p0, p1):
        x= numpy.array((p0))
        y= numpy.array((p1))
        dist = numpy.sqrt(numpy.sum((x-y)**2))
        return dist

    def centroid(l):
        results=[]
        if len(l)==1:
         
            for j in data1:
           
                if j[1]==l[0]:
                   
                    return j[0]
   
        if len(l)>1:
            for i in l:
                results.append(map(float, i))
            avg = [float(sum(col))/len(col) for col in zip(*results)]
      
            return avg
    combi = list(itertools.combinations(data1, 2))
    for p0,p1 in combi:
        euc_distance.append(list((distance(p0[0], p1[0]),[[int(p0[1]),int(p1[1])]])))
    for i in euc_distance:
        heapq.heappush(heap,list(i))
    euc_distance=[]
    
    for i in heap:
        i= list(i)


    while (True):
        euc_distance=[]
        if len(cluster)==int(k):
            break
        if len(heap)==0:
            print "Cluster number more than number of points"
            break
    
        elem1=heapq.heappop(heap)
        elem=elem1[1]
        ind=[]
        inbetween=[]
        c=0
        flag=0
        for i in cluster:
            for j in elem:
                if len(i)>=2 and len(j)>=2:
                    if i == j:
                        ind.append(cluster.index(i))
            
                if len(i)==1 and len(j)==1:
                    if i==j:
                        ind.append(cluster.index(i))

                if len(i)==1 and len(j)>=2:
                    s=len(j)
                    if i[0] in j:
                        flag=flag+1
                        inbetween.append(cluster.index(i))
                        if flag==s:
                            for x in inbetween:
                                ind.append(x)

        inbetween=[]
        flag=0
        ass=[]
        for i in ind:
            ass.append(cluster[i])

        newcluster = [x for x in cluster if x not in ass]


        set=0
        l1=[]
        l2=[]
        l3=[]
        if len(cluster)==len(newcluster)+1:
            newcluster.append(cluster[ind[0]])
            set=0
        if len(cluster)==len(newcluster)+2:
            l1=cluster[ind[0]]
            l2=cluster[ind[1]]
            l3=[l1,l2]
            newcluster.append(list(chain(*l3)))
            set=1



        if set==1:
            list(newcluster for newcluster,_ in groupby(newcluster))
            new_k = []
            for e in newcluster:
                if e not in new_k:
                    new_k.append(e)
            newcluster = new_k

            cluster=newcluster
            c=[]
            centroidlist=[]
            final=[]
            myc=[]
            qp=0
            for i in cluster:
                centroidlist=[]
                if len(i)==1:
               
               
                    final.append([centroid(i),i])
                elif len(i)>1:
                    for j in i:
                        for t in data1:
                            if j == t[1]:
                                centroidlist.append(t[0])
             
           
                    myc.append([centroidlist,i])
                    final.append([centroid(myc[qp][0]),myc[qp][1]])
                    qp=qp+1




            euc_distance=[]

            for i in final:
                if sorted(i[1])==sorted(list(chain(*elem))):
                    newc= i
            
            for i in final:
               
                if distance(newc[0],i[0]) != 0.0:
                    euc_distance.append( [ distance(newc[0],i[0]),[newc[1],i[1]] ] )

            for i in euc_distance:
                heapq.heappush(heap,i)
            heapq.heapify(heap)
                          
    if len(heap)!=0:
        dic={}
        goldpair=[]
        clusterpair=[]
        plist=[]
        plist1=[]
        plist2=[]
        d=[]

        data2=[]
        with open(inp, 'rb') as f:
            plist = [(line.rstrip('\n').split(',')[0:num_col]) for line in f.readlines()]
        for i in range(len(plist)):
            plist1.append(list((plist[i],i)))
            #  counter=0
        for i in plist1:
            d.append([i[0][num_col-1],i[1]])
        for i in d:
            dic.setdefault(i[0],[])
            dic[i[0]].append(i[1])
        for k,v in dic.iteritems():
            goldpair.append(list(itertools.combinations(v,2)))


        gp=list(chain(*goldpair))
        for i in cluster:
            clusterpair.append(list(itertools.combinations(i,2)))

        cp=list(chain(*clusterpair))
        correct=0
        for i in gp:
            for j in cp:
                if sorted(i)==sorted(j):
                    correct=correct+1
        systotal=len(cp)
        goldtotal=len(gp)
        if systotal==0:
            precision=0.0
        else:
            precision=float(correct)/float(systotal)
        recall=float(correct)/float(goldtotal)

        print precision
        print recall


        for i in cluster:
            print sorted(i)



if __name__ == "__main__":
    execute(sys.argv[1],sys.argv[2])