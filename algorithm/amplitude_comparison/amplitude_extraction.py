import pandas as pd
import csv
from os import system, getcwd
from os.path import join
from matplotlib import pyplot as plt
system('cls')

path = getcwd() + '\\algorithm\\amplitude_comparison\\'
file1 = 'amp_vs_run_ch1.csv'
file2 = 'amp_vs_run_ch2.csv'
file3 = 'amp_vs_run_ch3.csv'
file4 = 'amp_vs_run_ch4.csv'
file5 = 'amp_vs_run_ch5.csv'
file6 = 'amp_vs_run_ch6.csv'

with open(path + file1, 'r') as f:
    csvreader = csv.reader(f)
    cols = next(csvreader)
    data1 = []
    for row in csvreader:
        data1.append(row)
    data1 = pd.DataFrame(data1, columns=cols)
    # print(data1)

with open(path + file2, 'r') as f:
    csvreader = csv.reader(f)
    cols = next(csvreader)
    data2 = []
    for row in csvreader:
        data2.append(row)
    data2 = pd.DataFrame(data2, columns=cols)
    # print(data2)

with open(path + file3, 'r') as f:
    csvreader = csv.reader(f)
    cols = next(csvreader)
    data3 = []
    for row in csvreader:
        data3.append(row)
    data3 = pd.DataFrame(data3, columns=cols)
    # print(data3)

with open(path + file4, 'r') as f:
    csvreader = csv.reader(f)
    cols = next(csvreader)
    data4 = []
    for row in csvreader:
        data4.append(row)
    data4 = pd.DataFrame(data4, columns=cols)
    # print(data4)

with open(path + file5, 'r') as f:
    csvreader = csv.reader(f)
    cols = next(csvreader)
    data5 = []
    for row in csvreader:
        data5.append(row)
    data5 = pd.DataFrame(data5, columns=cols)
    # print(data5)

with open(path + file6, 'r') as f:
    csvreader = csv.reader(f)
    cols = next(csvreader)
    data6 = []
    for row in csvreader:
        data6.append(row)
    data6 = pd.DataFrame(data6, columns=cols)
    # print(data6)

data1 = data1.amp1.tolist()
data3 = data3.amp3.tolist()
data2 = data2.amp2.tolist()
data4 = data4.amp4.tolist()
data5 = data5.amp5.tolist()
data6 = data6.amp6.tolist()
data1 = [float(x) for x in data1]
data2 = [float(x) for x in data2]
data3 = [float(x) for x in data3]
data4 = [float(x) for x in data4]
data5 = [float(x) for x in data5]
data6 = [float(x) for x in data6]

# channel 1
threshold_h = 2
threshold_l = 1
plt.clf()
plt.figure(figsize=(20, 10))
plt.suptitle('Channel 1')
plt.xlabel('Run Number')
plt.ylabel('Amplitude')
plt.scatter(range(1, 1001), data1)
plt.hlines(threshold_h, 0, 1000, colors='r',
           linestyles='dashed', label='Threshold={0}'.format(threshold_h))
plt.hlines(threshold_l, 0, 1000, colors='g',
           linestyles='dashed', label='Threshold={0}'.format(threshold_l))
plt.legend()
# plt.show()
plt.savefig(path + 'amp_ch1.png')
plt.close()
temp = []
for x in data1:
    if x > threshold_h:
        pass
    elif x < threshold_l:
        pass
    else:
        temp.append(x)
data1 = (pd.DataFrame(temp)).describe()

# channel 2
threshold_h = 2.5
threshold_l = 1
plt.clf()
plt.figure(figsize=(20, 10))
plt.suptitle('Channel 2')
plt.xlabel('Run Number')
plt.ylabel('Amplitude')
plt.scatter(range(1, 1001), data2)
plt.hlines(threshold_h, 0, 1000, colors='r',
           linestyles='dashed', label='Threshold={0}'.format(threshold_h))
plt.hlines(threshold_l, 0, 1000, colors='g',
           linestyles='dashed', label='Threshold={0}'.format(threshold_l))
plt.legend()
# plt.show()
plt.savefig(path + 'amp_ch2.png')
plt.close()
temp = []
for x in data2:
    if x > threshold_h:
        pass
    elif x < threshold_l:
        pass
    else:
        temp.append(x)
data2 = (pd.DataFrame(temp)).describe()

# channel 3
threshold_h = 3
threshold_l = 1
plt.clf()
plt.figure(figsize=(20, 10))
plt.suptitle('Channel 3')
plt.xlabel('Run Number')
plt.ylabel('Amplitude')
plt.scatter(range(1, 1001), data3)
plt.hlines(threshold_h, 0, 1000, colors='r',
           linestyles='dashed', label='Threshold={0}'.format(threshold_h))
plt.hlines(threshold_l, 0, 1000, colors='g',
           linestyles='dashed', label='Threshold={0}'.format(threshold_l))
plt.legend()
# plt.show()
plt.savefig(path + 'amp_ch3.png')
plt.close()
temp = []
for x in data3:
    if x > threshold_h:
        pass
    elif x < threshold_l:
        pass
    else:
        temp.append(x)
data3 = (pd.DataFrame(temp)).describe()

# channel 4
threshold_h = 3
threshold_l = 1
plt.clf()
plt.figure(figsize=(20, 10))
plt.suptitle('Channel 4')
plt.xlabel('Run Number')
plt.ylabel('Amplitude')
plt.scatter(range(1, 1001), data4)
plt.hlines(threshold_h, 0, 1000, colors='r',
           linestyles='dashed', label='Threshold={0}'.format(threshold_h))
plt.hlines(threshold_l, 0, 1000, colors='g',
           linestyles='dashed', label='Threshold={0}'.format(threshold_l))
plt.legend()
# plt.show()
plt.savefig(path + 'amp_ch4.png')
plt.close()
temp = []
for x in data4:
    if x > threshold_h:
        pass
    elif x < threshold_l:
        pass
    else:
        temp.append(x)
data4 = (pd.DataFrame(temp)).describe()

# channel 5
threshold_h = 3
threshold_l = 1.5
plt.clf()
plt.figure(figsize=(20, 10))
plt.suptitle('Channel 5')
plt.xlabel('Run Number')
plt.ylabel('Amplitude')
plt.scatter(range(1, 1001), data5)
plt.hlines(threshold_h, 0, 1000, colors='r',
           linestyles='dashed', label='Threshold={0}'.format(threshold_h))
plt.hlines(threshold_l, 0, 1000, colors='g',
           linestyles='dashed', label='Threshold={0}'.format(threshold_l))
plt.legend()
# plt.show()
plt.savefig(path + 'amp_ch5.png')
plt.close()
temp = []
for x in data5:
    if x > threshold_h:
        pass
    elif x < threshold_l:
        pass
    else:
        temp.append(x)
data5 = (pd.DataFrame(temp)).describe()

# channel 6
threshold_h = 2
threshold_l = 1
plt.clf()
plt.figure(figsize=(20, 10))
plt.suptitle('Channel 6')
plt.xlabel('Run Number')
plt.ylabel('Amplitude')
plt.scatter(range(1, 1001), data6)
plt.hlines(threshold_h, 0, 1000, colors='r',
           linestyles='dashed', label='Threshold={0}'.format(threshold_h))
plt.hlines(threshold_l, 0, 1000, colors='g',
           linestyles='dashed', label='Threshold={0}'.format(threshold_l))
plt.legend()
# plt.show()
plt.savefig(path + 'amp_ch6.png')
plt.close()
temp = []
for x in data6:
    if x > threshold_h:
        pass
    elif x < threshold_l:
        pass
    else:
        temp.append(x)
data6 = (pd.DataFrame(temp)).describe()

# combine
data = pd.concat([data1, data2, data3, data4, data5, data6], axis=1)
data.columns = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6']
data.to_csv(path + 'amp.csv')
