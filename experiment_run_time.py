import time
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


def runningTime(running_times):
    totalTime = 0
    for i in range(len(running_times)):
        totalTime += running_times[i]

    standard_dev = standardDeviation(running_times)
    N = len(running_times)
    m = totalTime / N
    t_value_90 = 1.660
    t_value_95 = 1.984
    standard_error = standardError(standard_dev, N)
    upper_mean_90 = m + t_value_90 * standard_error
    lower_mean_90 = m - t_value_90 * standard_error
    upper_mean_95 = m + t_value_95 * standard_error
    lower_mean_95 = m - t_value_95 * standard_error
    return [m, standard_dev, standard_error, lower_mean_90, upper_mean_90, lower_mean_95, upper_mean_95]


def Compress2strings(ind, edges):
    a = edges[ind][0]
    b = edges[ind][1]
    i = len(edges) - 1
    while i != -1:
        if edges[i][0] == a:  # Remove edges start with a
            del edges[i]
        elif edges[i][1] == b:  # Remove edges end with b
            del edges[i]
        elif edges[i][0] == b:  # Edges which which b goes are now goes from X
            if edges[i][1] == a:
                del edges[i]
            else:
                edges[i][0] = a
        i = i - 1  # Edges which goes to a, now goes to this new X
    return


def overlap(a, b):
    # return length of longest suffix of a which matches prefix of w
    start = 0
    while True:
        start = a.find(b[0], start)
        if start == -1:
            return 0
        if b.startswith(a[start:]):
            return len(a) - start
        start += 1


from itertools import permutations


def FindAllOverlaps(Set):
    Edges = []
    for a, b in permutations(range(len(Set)), 2):
        W = overlap(Set[a], Set[b])
        if W > 0:
            Edges.append([a, b, W])
    return Edges


def SCSS(Edges):  # GREEDY
    Total_Path_Weight = 0
    while (len(Edges) != 0):
        # Find Longest Weight & its index
        maxWeight = 0
        index = -1
        for E in range(len(Edges)):
            if Edges[E][2] > maxWeight:
                maxWeight = Edges[E][2]
                index = E

        Total_Path_Weight += maxWeight
        Compress2strings(index, Edges)

    return Total_Path_Weight


def Eliminate_Substr(SS):
    i = 0
    while i != len(SS):
        t = i + 1
        while t != len(SS):
            if (SS[t] in SS[i]):
                del SS[t]
            elif (SS[i] in SS[t]):
                del SS[i]
                i -= 1
                break
            else:
                t += 1
        i += 1
    return


def Check(Str_Set, k):
    Eliminate_Substr(Str_Set)
    Total_Len = 0
    for st in Strings:
        Total_Len += len(st)
    E = FindAllOverlaps(Strings)
    SCSS_len = Total_Len - SCSS(E)
    if k >= SCSS_len:
        return True
    return False


time_arr = []
size = []
stan_dev_arr = []
stan_err_arr = []
conf_lev_90 = []
conf_lev_95 = []

for i in range(20):

    running_times = []
    for m in range(run_size):
        start_time = time.time()
        Strings = []
        for x in range((i + 1) * 5):
            a = "{0:010b}".format(random.getrandbits(10))
            Strings.append(a)

        no_of_strings = (i + 1) * 5
        k = 6 * no_of_strings
        Check(Strings, k)
        elapsed_time = time.time() - start_time
        running_times.append(elapsed_time)

    run_time_array = runningTime(running_times)
    time_arr.append(run_time_array[0])
    size.append(no_of_strings)
    stan_dev_arr.append((run_time_array[1]))
    stan_err_arr.append(run_time_array[2])
    run_time_array[3] = "{0:.5f}".format(run_time_array[3])
    run_time_array[4] = "{0:.5f}".format(run_time_array[4])
    run_time_array[5] = "{0:.5f}".format(run_time_array[5])
    run_time_array[6] = "{0:.5f}".format(run_time_array[6])
    conf_lev_90.append(str(run_time_array[3]) + "-" + str(run_time_array[4]))
    conf_lev_95.append(str(run_time_array[5]) + "-" + str(run_time_array[6]))



plt.plot(size, time_arr)
plt.title('Mean Time Comparison Based on Array Size for ' + str(run_size) + " Runs")
plt.xlabel('Array Size')
plt.ylabel('Mean Time')
plt.savefig('plot-array-size-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)
headers = ["Array Size","Mean Time", "Standard Deviation", "Standard Error", "90% Confidence Level", "95% Confidence Level"]

data = []
for item in range(len(size)):
    data.append((size[item],time_arr[item],stan_dev_arr[item], stan_err_arr[item], conf_lev_90[item], conf_lev_95[item]))

print(tabulate(data, headers=headers))

data_arr = []
for i in range(len(data)):
    data_arr.append(data[i])

plt.cla()
plt.clf()
plt.title('Mean Time Based on Array Size for ' + str(run_size) + " Runs")
the_table = plt.table(cellText=data_arr, colLabels=headers, loc='center')
for x in range(len(headers)):
    the_table.auto_set_column_width(x)
the_table.auto_set_font_size(False)
the_table.set_fontsize(5)
the_table.scale(1, 1)
# Removing ticks and spines enables you to get the figure only with table
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('table-array-size-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)

#####

time_arr = []
str_len = []
stan_dev_arr = []
stan_err_arr = []
conf_lev_90 = []
conf_lev_95 = []
for str_size in range(5, 105, 5):

    running_times_size = []


    no_of_strings = 20
    k = 6 * no_of_strings
    count = 0
    for i in range(run_size):
        Strings = []
        start_time = time.time()
        for x in range(20):
            str_shift = "{0:0" + str(str_size) + "b}"
            a = str_shift.format(random.getrandbits(str_size))
            Strings.append(a)

        Check(Strings, k)
        elapsed_time = time.time() - start_time
        running_times_size.append(elapsed_time)

    run_time_array = runningTime(running_times_size)
    time_arr.append(run_time_array[0])
    str_len.append(str_size)
    stan_dev_arr.append((run_time_array[1]))
    stan_err_arr.append(run_time_array[2])
    run_time_array[1] = "{0:.5f}".format(run_time_array[1])
    run_time_array[2] = "{0:.5f}".format(run_time_array[2])
    run_time_array[3] = "{0:.5f}".format(run_time_array[3])
    run_time_array[4] = "{0:.5f}".format(run_time_array[4])
    run_time_array[5] = "{0:.5f}".format(run_time_array[5])
    run_time_array[6] = "{0:.5f}".format(run_time_array[6])
    conf_lev_90.append(str(run_time_array[3]) + "-" + str(run_time_array[4]))
    conf_lev_95.append(str(run_time_array[5]) + "-" + str(run_time_array[6]))

plt.cla()
plt.clf()
plt.plot(str_len, time_arr)
plt.title('Mean Time Comparison Based on String Size for ' + str(run_size) + " Runs")
plt.xlabel('String size')
plt.ylabel('Mean Time')
plt.savefig('plot-string-size-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)

headers = ["String Size","Mean Time", "Standard Deviation", "Standard Error", "90% Confidence Level", "95% Confidence Level"]

data = []
for m in range(len(str_len)):
    data.append((str_len[m],time_arr[m], stan_dev_arr[m], stan_err_arr[m], conf_lev_90[m], conf_lev_95[m]))
print(tabulate(data, headers=headers))
data_arr = []
for i in range(len(str_len)):
    data_arr.append(data[i])
plt.cla()
plt.clf()
plt.title('Mean Time Based on String Size for ' + str(run_size) + " Runs")
the_table = plt.table(cellText=data_arr, colLabels=headers, loc='center')
for x in range(len(headers)):
    the_table.auto_set_column_width(x)
the_table.auto_set_font_size(False)
the_table.set_fontsize(5)
the_table.scale(1, 1)
# Removing ticks and spines enables you to get the figure only with table
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('table-string-size-'+str(run_size)+'.png', bbox_inches='tight', pad_inches=0.05)



