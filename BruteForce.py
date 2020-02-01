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

from itertools import permutations
def FindAllOverlaps(Set):
    Edges= [] 
    for a,b in permutations(range(len(Set)),2):
        W = overlap(Set[a],Set[b])
        if W > 0:
            Edges.append([a,b,W])
    return Edges

def SCSS(Edges): #GREEDY
    Total_Path_Weight = 0
    while (len(Edges) != 0):
        #Find Longest Weight & its index
        maxWeight = 0
        index = -1
        for E in range (len(Edges)):
            if Edges[E][2] > maxWeight:
                maxWeight = Edges[E][2]
                index = E

        Total_Path_Weight += maxWeight
        Compress2strings(index,Edges)

    return Total_Path_Weight

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

def BruteForce(Set,Edges):
    maxW = 0
    for i in (permutations(range(Set),Set)):
        currW=0
        for t in range (Set-1):
            for e in Edges:
                if i[t] == e[0] and i[t+1] == e[1]:
                    currW += e[2]
                    break
        if currW > maxW:
            maxW = currW
    return maxW

def Check(Str_Set,k):
    Eliminate_Substr(Str_Set)
    Total_Len = 0
    for st in Strings:
        Total_Len += len(st)
    E = FindAllOverlaps(Strings)
    SCSS_len = Total_Len - SCSS(E)
    E = FindAllOverlaps(Strings)
    BruteForce_len = Total_Len - BruteForce(len(Str_Set),E)
   
    if k >= SCSS_len:
        return True , (BruteForce_len,SCSS_len)
    return False , (BruteForce_len,SCSS_len)



#Strings= ["101010100011","110101010","101110","011001" ,"11101011",]
#Strings= ["101010100011","01010","00011","101"] Substr test
import random

word = ""
Strings=[]
for i in range (0,10):
    strlength = random.randint(0,20)
    print ("strlength is : ", strlength)
    for j in range (0,strlength):
        ran = random.randint(0,1)
        str(ran)
        word += str(ran)
    
    print ("word is : ", word)
    Strings.append(word)
    word = ""
    
print ("Array is : ",Strings)


bl , tp = Check(Strings,2100)
if(bl):
    print("SUCCESS")
else: print("FAIL")

if(tp[0] < tp[1]):
    print("Brute Force is shorter :(")
    print("Brute force length: ",tp[0],"Greedy Length: ",tp[1])
else: 
    print("en büyük asker bizim asker")
    print("Brute force length: ",tp[0],"Greedy Length: ",tp[1])
