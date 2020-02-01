from itertools import permutations

def Compress2strings(ind,edges):
    a = edges[ind][0]
    b = edges[ind][1]
    i = len(edges)-1
    while i != -1:
        if   edges[i][0] == a:         #Remove edges start with a
            del edges[i]
        elif edges[i][1] == b:         #Remove edges end with b
            del edges[i]
        elif edges[i][0] == b:         #Edges which which b goes are now goes from X
            if edges[i][1] == a:
                del edges[i]
            else:
                edges[i][0] = a
        i = i-1                        #Edges which goes to a, now goes to this new X
    return 

def  overlap(a,b):
    #return length of longest suffix of a which matches prefix of w
    start = 0
    while True:
        start = a.find(b[0],start)
        if start == -1:
            return 0
        if b.startswith(a[start:]):
            return len(a)-start
        start += 1

def FindAllOverlaps(Set):
    Edges= [] 
    for a,b in permutations(range(len(Set)),2):
        W = overlap(Set[a],Set[b])
        if W > 0:
            Edges.append([a,b,W])
    return Edges

def SCSS(Edges): #Greedy Algorithm for finding shortest common superstring
    Total_Path_Weight = 0
    ChosenEdges = []
    while (len(Edges) != 0):
        maxWeight = 0
        index = -1
        for E in range (len(Edges)): #Find Longest Weight & its index
            if Edges[E][2] > maxWeight:
                maxWeight = Edges[E][2]
                index = E
        Total_Path_Weight += maxWeight
        ChosenEdges.append(Edges[index])
        Compress2strings(index,Edges)
    return Total_Path_Weight, ChosenEdges

def Eliminate_Substr(SS):
    i=0
    while i != len(SS):
        t = i+1
        while t != len(SS):
            if(SS[t] in SS[i]):
                del SS[t]
            elif(SS[i] in SS[t]):
                del SS[i]
                i -= 1
                break
            else: t += 1
        i += 1
    return

def CombineEdges(Edges,STR):
    for E in Edges:
        STR[E[0]] =  STR[E[0]]    +   STR[E[1]][E[2]:]
        STR[E[1]] = ""

    SS = ""
    for s in STR:
        if s != "":  SS += s 
    return SS


def Check(Str_Set,k):
    Eliminate_Substr(Str_Set) #Eliminate substrings on the Set
    Total_Len = 0
    for st in Strings:
        Total_Len += len(st)
    E = FindAllOverlaps(Strings)
    Overlap_Length, E2 = SCSS(E)
    SCSS_len = Total_Len - Overlap_Length
    SS = CombineEdges(E2,Strings)
    if k >= SCSS_len:
        return True ,SS
    return False ,SS


import random
word = ""
Strings=[]
numstr = random.randint(4,8)        #number of the strings
for i in range (0,numstr):                    
    strlength = random.randint(4,6) #string length
    #print ("strlength is : ", strlength)
    for j in range (0,strlength):
        ran = random.randint(0,1)
        str(ran)
        word += str(ran)
    
    #print ("word is : ", word)
    Strings.append(word)
    word = ""
print ("Array is : ",Strings)

k = 100


#Strings =["011","100","001","010"]
Arr = Strings.copy()

Bl , SS = Check(Strings,k)
for x  in Strings:
    if x not in SS:
        print("Fail!")
print("superstring is:", SS)


def verify(Arr, SS):
    count = 0
    for s in Arr:
        for i in range(len(SS)):
            if(s == SS[i:i+len(s)]):
                count = count + 1
                break
    if(count == len(Arr)):
        print('Correct')    
    else: print ("Not-Correct")    

verify(Arr, SS)



if(Bl):
    print("SUCCESS")
else: print("FAIL")