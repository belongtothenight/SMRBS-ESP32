from alg import PE
import datetime

export_path = '/home/pi/SMRBS-ESP32/algorithm/pe_comparison/run7/'
export_summary_fn = 'summary.txt'
chunk = 500

def init_sumfile():
    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d:%H:%M:%S")
    with open(export_path + export_summary_fn, 'w', encoding='utf-8') as f:
        f.write('>> Experiment detail:\n')
        f.write('Put the speaker at the relatively same location as the different microphones to see whether all microphones have the same gain.\n')
        f.write('\n')
        f.write('>> Experiment setup:\n')
        f.write('source: smartphone --bluetooth--> speaker\n')
        f.write('volume: max * 1 https://noises.online/\n')
        f.write('signal_type: white noise\n')
        f.write('signal_frequency_hz: N/A\n')
        f.write('sampling_rate_hz: 16000\n')
        f.write('distance_cm: 10\n')
        f.write('height_cm: -3 (on table)\n')
        f.write('run: 1\n')
        f.write('\n')
        f.write('>> Figure:\n')
        f.write('content: power estimation result of each individual channel\n')
        f.write('x-axis: samples\n')
        f.write('y-axis: Watt\n')
        f.write('title: the channel facing the audio source\n')
        f.write('legend: final power estimation value of each channel\n')
        f.write('\n')
        f.write('>> Result: ({0})\n'.format(now))
        

if __name__ == '__main__':
    pe = PE(chunk_=chunk)
    i = -1
    ch = []
    export_lines = {1:'', 2:'', 3:'', 4:'', 5:'', 6:''}
    while True:
        num = input(
            '\nEnter number of testing channel: (\'q\' to quit, \'e\' export plots) ')
        i += 1
        if num == 'q':
            # quit program
            break
        elif num == 'e':
            # export plots & lines
            for j in range(i):
                pe.plt_pe1(maxch=ch[j], fi=j,
                               fn=export_path)
            # export lines
            init_sumfile()
            with open(export_path + export_summary_fn, 'a', encoding='utf-8') as f:
                for j in range(len(export_lines)):
                    f.write(export_lines[j+1])
            pe.clear_data()
            i = -1
            ch = []
        else:
            num = int(num)
            ch.append(num)
            pe.read_data()
            pe.pow()
            pe.pe1()
            pe.dc1()
            pe.store_data()
            # get export lines
            pe1data = [
                pe.mem_pe11[-1][-1],
                pe.mem_pe12[-1][-1],
                pe.mem_pe13[-1][-1],
                pe.mem_pe14[-1][-1],
                pe.mem_pe15[-1][-1],
                pe.mem_pe16[-1][-1],
                ]
            max_ch = 1 + pe1data.index(max(pe1data))
            l = '{0} >> {1} >> pe: {2:.4f} / {3:.4f} / {4:.4f} / {5:.4f} / {6:.4f} / {7:.4f}\n'.format(
                    num, max_ch, pe1data[0], pe1data[1], pe1data[2], pe1data[3], pe1data[4], pe1data[5]
                )
            export_lines[num] = l
    pe.terminate()
    del pe
    print('\nFinished executing!')
