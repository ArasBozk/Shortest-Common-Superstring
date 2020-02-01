import random
import math
from matplotlib import pyplot as plt
from tabulate import tabulate
run_size=100
def standardDeviation(results):
    sum = 0
    mean = 0
    standard_deviation = 0
    for i in range(len(results)):
        sum += results[i]

    mean = sum / len(results)

    for j in range(len(results)):
        standard_deviation += pow(results[j] - mean, 2)

    standard_deviation = math.sqrt(standard_deviation / len(results))
    return standard_deviation


def standardError(standard_deviation, n):
    return standard_deviation / math.sqrt(n)

def calculateStatistics(len_size):
    total = 0
    for i in range(len(len_size)):
        total += len_size[i]

    standard_dev = standardDeviation(len_size)
    N = len(len_size)
    m = total / N
    t_value_90 = 1.660
    t_value_95 = 1.984
    standard_error = standardError(standard_dev, N)
    upper_mean_90 = m + t_value_90 * standard_error
    lower_mean_90 = m - t_value_90 * standard_error
    upper_mean_95 = m + t_value_95 * standard_error
    lower_mean_95 = m - t_value_95 * standard_error
    return [m, standard_dev, standard_error, lower_mean_90, upper_mean_90, lower_mean_95, upper_mean_95]


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
    #E = FindAllOverlaps(Strings)
    #BruteForce_len = Total_Len - BruteForce(len(Str_Set),E)
    return SCSS_len


lenght_array=[]
stan_dev_arr = []
stan_err_arr = []
conf_lev_90 = []
conf_lev_95 = []
size = []
for i in range(20):


    len_size = []

    for m in range(run_size):
        Strings = []
        for x in range((i + 1) * 5):
            a = "{0:010b}".format(random.getrandbits(10))
            Strings.append(a)
        k = len(Strings)
        len_size.append(Check(Strings, k))
    no_of_strings = (i+1)*5
    len_array = calculateStatistics(len_size)
    lenght_array.append(len_array[0])
    size.append(no_of_strings)
    len_array[1] = "{0:.5f}".format(len_array[1])
    len_array[2] = "{0:.5f}".format(len_array[2])
    stan_dev_arr.append(len_array[1])
    stan_err_arr.append(len_array[2])
    len_array[3] = "{0:.4f}".format(len_array[3])
    len_array[4] = "{0:.4f}".format(len_array[4])
    len_array[5] = "{0:.4f}".format(len_array[5])
    len_array[6] = "{0:.4f}".format(len_array[6])
    conf_lev_90.append(str(len_array[3]) + "-" + str(len_array[4]))
    conf_lev_95.append(str(len_array[5]) + "-" + str(len_array[6]))

plt.cla()
plt.clf()
plt.plot(size, lenght_array)
plt.title('Mean Length Comparison Based on Array Size for ' + str(run_size) + " Runs")
plt.xlabel('Array Size')
plt.ylabel('Mean Length')
plt.savefig('plot-array-size-len-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)
headers = ["Array Size","Mean Length", "Standard Deviation", "Standard Error", "90% Confidence Level", "95% Confidence Level"]
data=[]
for item in range(len(size)):
    data.append((size[item],lenght_array[item],stan_dev_arr[item], stan_err_arr[item], conf_lev_90[item], conf_lev_95[item]))

print(tabulate(data, headers=headers))
data_arr = []
for i in range(len(data)):
    data_arr.append(data[i])

plt.cla()
plt.clf()
plt.title('Mean Length Based on Array Size for ' + str(run_size) + " Runs")
the_table = plt.table(cellText=data_arr, colLabels=headers, loc='center')
for x in range(len(headers)):
    the_table.auto_set_column_width(x)
the_table.auto_set_font_size(False)
the_table.set_fontsize(5)
the_table.scale(1, 1)
# Removing ticks and spines to get the figure only with table
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('table-array-size-len-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)


lenght_array=[]
stan_dev_arr = []
stan_err_arr = []
conf_lev_90 = []
conf_lev_95 = []
str_len = []
for str_size in range(5,105,5):

    len_size = []

    for m in range(run_size):
        Strings = []
        for x in range(20):
            str_shift = "{0:0" + str(str_size) + "b}"
            a = str_shift.format(random.getrandbits(str_size))
            Strings.append(a)

        k = 6 * str_size
        len_size.append(Check(Strings, k))

    len_array = calculateStatistics(len_size)
    lenght_array.append(len_array[0])
    str_len.append(str_size)
    len_array[1] = "{0:.5f}".format(len_array[1])
    len_array[2] = "{0:.5f}".format(len_array[2])
    stan_dev_arr.append(len_array[1])
    stan_err_arr.append(len_array[2])
    len_array[3] = "{0:.4f}".format(len_array[3])
    len_array[4] = "{0:.4f}".format(len_array[4])
    len_array[5] = "{0:.4f}".format(len_array[5])
    len_array[6] = "{0:.4f}".format(len_array[6])
    conf_lev_90.append(str(len_array[3]) + "-" + str(len_array[4]))
    conf_lev_95.append(str(len_array[5]) + "-" + str(len_array[6]))

plt.cla()
plt.clf()
plt.plot(str_len, lenght_array)
plt.title('Mean Length Comparison Based on String Size for ' + str(run_size) + " Runs")
plt.xlabel('String Length')
plt.ylabel('Mean Length')
plt.savefig('plot-string-size-len-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)
headers = ["String Length","Mean Length", "Standard Deviation", "Standard Error", "90% Confidence Level", "95% Confidence Level"]
data=[]
for item in range(len(str_len)):
    data.append((str_len[item],lenght_array[item],stan_dev_arr[item], stan_err_arr[item], conf_lev_90[item], conf_lev_95[item]))

print(tabulate(data, headers=headers))
data_arr = []
for i in range(len(data)):
    data_arr.append(data[i])

plt.cla()
plt.clf()
plt.title('Mean Length Based on String Size for ' + str(run_size) + " Runs")
the_table = plt.table(cellText=data_arr, colLabels=headers, loc='center')
for x in range(len(headers)):
    the_table.auto_set_column_width(x)
the_table.auto_set_font_size(False)
the_table.set_fontsize(5)
the_table.scale(1, 1)
# Removing ticks and spines to get the figure only with table
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('table-string-size-len-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)



lenght_array=[]
stan_dev_arr = []
stan_err_arr = []
conf_lev_90 = []
conf_lev_95 = []
size = []
for i in range(20):


    len_size = []

    for m in range(run_size):
        word = ""
        Strings = []
        for k in range(20):
            strlength = random.randint(i*5,(i+1)*5)
            for j in range(0, strlength):
                ran = random.randint(0, 1)
                str(ran)
                word += str(ran)

            Strings.append(word)
            word = ""

        k = len(Strings)
        len_size.append(Check(Strings, k))
    no_of_strings = str(i*5) + "-"+ str((i+1)*5)
    len_array = calculateStatistics(len_size)
    lenght_array.append(len_array[0])
    size.append(no_of_strings)
    len_array[1] = "{0:.5f}".format(len_array[1])
    len_array[2] = "{0:.5f}".format(len_array[2])
    stan_dev_arr.append(len_array[1])
    stan_err_arr.append(len_array[2])
    len_array[3] = "{0:.4f}".format(len_array[3])
    len_array[4] = "{0:.4f}".format(len_array[4])
    len_array[5] = "{0:.4f}".format(len_array[5])
    len_array[6] = "{0:.4f}".format(len_array[6])
    conf_lev_90.append(str(len_array[3]) + "-" + str(len_array[4]))
    conf_lev_95.append(str(len_array[5]) + "-" + str(len_array[6]))

plt.cla()
plt.clf()
plt.plot(size, lenght_array)
plt.title('Mean Length Comparison Based on String Intervals for ' + str(run_size) + " Runs")
plt.xticks(rotation=90)
plt.xlabel('String Interval')
plt.ylabel('Mean Length')
plt.savefig('plot-str-size-interval-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)
headers = ["String Interval","Mean Length", "Standard Deviation", "Standard Error", "90% Confidence Level", "95% Confidence Level"]
data=[]
for item in range(len(size)):
    data.append((size[item],lenght_array[item],stan_dev_arr[item], stan_err_arr[item], conf_lev_90[item], conf_lev_95[item]))

print(tabulate(data, headers=headers))
data_arr = []
for i in range(len(data)):
    data_arr.append(data[i])

plt.cla()
plt.clf()
plt.title('Mean Length Based on String Intervals for ' + str(run_size) + " Runs")
the_table = plt.table(cellText=data_arr, colLabels=headers, loc='center')
for x in range(len(headers)):
    the_table.auto_set_column_width(x)
the_table.auto_set_font_size(False)
the_table.set_fontsize(5)
the_table.scale(1, 1)
# Removing ticks and spines to get the figure only with table
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('table-str-len-interval-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)
