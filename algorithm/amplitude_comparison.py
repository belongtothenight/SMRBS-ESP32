from alg import PE
from matplotlib import pyplot as plt
from time import sleep
import pandas as pd

chunk = 50  # roughly a sine wave period of 500 Hz
export_path = '/home/pi/code_alg/amplitude_comparison/'

data1 = []
data2 = []
data3 = []
data4 = []
data5 = []
data6 = []

# set recording mod
mod = input(
    '\nRecording mod: \n1. fresh start \n2. keep alive \n3. terminate \nOption: ')
if mod == '1':
    pass
elif mod == '2':
    pe = PE(chunk_=chunk)
    for i in range(20):
        pe.read_data()
elif mod == '3':
    quit()

# set runs
runs = input(
    '\nHow many runs? \n\'d\' is default 50 \n\'q\' to quit \ninteger \nOption: ')
if runs == 'd':
    runs = 50
elif runs == 'q':
    quit()
else:
    runs = int(runs)

# main loop
while True:
    num = input('\nEnter number of testing channel: (\'q\' to quit) ')
    if mod == '1':
        pe = PE(chunk_=chunk)
    if num == 'q':
        break
    for i in range(runs):
        pe.read_data()
        # pe.plt_s()
        max1 = round(max(pe.d1), 3)
        max2 = round(max(pe.d2), 3)
        max3 = round(max(pe.d3), 3)
        max4 = round(max(pe.d4), 3)
        max5 = round(max(pe.d5), 3)
        max6 = round(max(pe.d6), 3)
        min1 = round(min(pe.d1), 3)
        min2 = round(min(pe.d2), 3)
        min3 = round(min(pe.d3), 3)
        min4 = round(min(pe.d4), 3)
        min5 = round(min(pe.d5), 3)
        min6 = round(min(pe.d6), 3)
        mid1 = round(max1 + min1, 3)
        mid2 = round(max2 + min2, 3)
        mid3 = round(max3 + min3, 3)
        mid4 = round(max4 + min4, 3)
        mid5 = round(max5 + min5, 3)
        mid6 = round(max6 + min6, 3)
        amp1 = round(max1 - min1, 3)
        amp2 = round(max2 - min2, 3)
        amp3 = round(max3 - min3, 3)
        amp4 = round(max4 - min4, 3)
        amp5 = round(max5 - min5, 3)
        amp6 = round(max6 - min6, 3)
        print('Run: ', i+1)
        # print('max: ', max1, max2, max3, max4, max5, max6)
        # print('min: ', min1, min2, min3, min4, min5, min6)
        # print('mid: ', mid1, mid2, mid3, mid4, mid5, mid6)
        # print('amp: ', amp1, amp2, amp3, amp4, amp5, amp6)
        data1.append([max1, min1, mid1, amp1])
        data2.append([max2, min2, mid2, amp2])
        data3.append([max3, min3, mid3, amp3])
        data4.append([max4, min4, mid4, amp4])
        data5.append([max5, min5, mid5, amp5])
        data6.append([max6, min6, mid6, amp6])

    max1 = [i[0] for i in data1]
    min1 = [i[1] for i in data1]
    mid1 = [i[2] for i in data1]
    amp1 = [i[3] for i in data1]
    max2 = [i[0] for i in data2]
    min2 = [i[1] for i in data2]
    mid2 = [i[2] for i in data2]
    amp2 = [i[3] for i in data2]
    max3 = [i[0] for i in data3]
    min3 = [i[1] for i in data3]
    mid3 = [i[2] for i in data3]
    amp3 = [i[3] for i in data3]
    max4 = [i[0] for i in data4]
    min4 = [i[1] for i in data4]
    mid4 = [i[2] for i in data4]
    amp4 = [i[3] for i in data4]
    max5 = [i[0] for i in data5]
    min5 = [i[1] for i in data5]
    mid5 = [i[2] for i in data5]
    amp5 = [i[3] for i in data5]
    max6 = [i[0] for i in data6]
    min6 = [i[1] for i in data6]
    mid6 = [i[2] for i in data6]
    amp6 = [i[3] for i in data6]

    fig, axs = plt.subplots(2, 3, figsize=(20, 10))
    fig.suptitle('Amplitude vs Run')
    fig.tight_layout(pad=3.0, h_pad=3.0, w_pad=3.0)
    axs[0, 0].plot(max1, 'r', label='max')
    axs[0, 0].plot(min1, 'b', label='min')
    axs[0, 0].plot(mid1, 'g', label='mid')
    axs[0, 0].plot(amp1, 'y', label='amp')
    axs[0, 0].set_title('Channel 1')
    axs[0, 0].legend()
    axs[0, 1].plot(max2, 'r', label='max')
    axs[0, 1].plot(min2, 'b', label='min')
    axs[0, 1].plot(mid2, 'g', label='mid')
    axs[0, 1].plot(amp2, 'y', label='amp')
    axs[0, 1].set_title('Channel 2')
    axs[0, 1].legend()
    axs[0, 2].plot(max3, 'r', label='max')
    axs[0, 2].plot(min3, 'b', label='min')
    axs[0, 2].plot(mid3, 'g', label='mid')
    axs[0, 2].plot(amp3, 'y', label='amp')
    axs[0, 2].set_title('Channel 3')
    axs[0, 2].legend()
    axs[1, 0].plot(max4, 'r', label='max')
    axs[1, 0].plot(min4, 'b', label='min')
    axs[1, 0].plot(mid4, 'g', label='mid')
    axs[1, 0].plot(amp4, 'y', label='amp')
    axs[1, 0].set_title('Channel 4')
    axs[1, 0].legend()
    axs[1, 1].plot(max5, 'r', label='max')
    axs[1, 1].plot(min5, 'b', label='min')
    axs[1, 1].plot(mid5, 'g', label='mid')
    axs[1, 1].plot(amp5, 'y', label='amp')
    axs[1, 1].set_title('Channel 5')
    axs[1, 1].legend()
    axs[1, 2].plot(max6, 'r', label='max')
    axs[1, 2].plot(min6, 'b', label='min')
    axs[1, 2].plot(mid6, 'g', label='mid')
    axs[1, 2].plot(amp6, 'y', label='amp')
    axs[1, 2].set_title('Channel 6')
    axs[1, 2].legend()
    plt.savefig(export_path + 'amp_vs_run_ch{0}.png'.format(num))
    plt.close()

    data = pd.DataFrame({'max1': max1, 'min1': min1, 'mid1': mid1, 'amp1': amp1,
                        'max2': max2, 'min2': min2, 'mid2': mid2, 'amp2': amp2,
                         'max3': max3, 'min3': min3, 'mid3': mid3, 'amp3': amp3,
                         'max4': max4, 'min4': min4, 'mid4': mid4, 'amp4': amp4,
                         'max5': max5, 'min5': min5, 'mid5': mid5, 'amp5': amp5,
                         'max6': max6, 'min6': min6, 'mid6': mid6, 'amp6': amp6})
    data.to_csv(export_path + 'amp_vs_run_ch{0}.csv'.format(num), index=False)

    data = data.describe()
    data.to_csv(export_path + 'amp_vs_run_stats_ch{0}.csv'.format(num))

    del max1, min1, mid1, amp1, max2, min2, mid2, amp2, max3, min3, mid3, amp3, max4, min4, mid4, amp4, max5, min5, mid5, amp5, max6, min6, mid6, amp6
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []

    if mod == '1':
        pe.terminate()
        del pe

if mod == '2':
    pe.terminate()
    del pe
