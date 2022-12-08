import datetime
import os

def init_directory(path_select=1):
    while True:
        exp_num = input(
            'Enter experiment run number: (number, \'q\' to quit) ')
        if path_select == 1:
            export_path = '/home/pi/SMRBS-ESP32/algorithm/pe_comparison/run{0}/'.format(
                exp_num)
        elif path_select == 2:
            export_path = '/home/pi/SMRBS-ESP32/algorithm/fair_comparison/nr{0}/'.format(
                exp_num)
        export_summary_fn = 'summary.txt'
        if exp_num == 'q':
            exit()
        elif os.path.exists(export_path):
            print('Folder already exist, delete it or give it a different number.')
            print('Content of the folder:')
            for (dirpath, dirnames, filenames) in os.walk(export_path):
                print('dirpath: {0}'.format(dirpath))
                print('dirnames: {0}'.format(dirnames))
                print('filenames: {0}'.format(filenames))
            option = input('"y" to over write, "r" to re-enter, "q" to quit: ')
            if option == 'y':
                os.system('rm -rf {0}'.format(export_path))
                os.system('mkdir {0}'.format(export_path))
                break
            elif option == 'r':
                continue
            elif option == 'q':
                exit()

        else:
            os.mkdir(export_path)
            break
    return export_path, export_summary_fn


def init_sumfile(samp_dp, samp_ds, chunk, alpha, fp, fn):
    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d:%H:%M:%S")
    lines = [
        '>> Experiment detail (NR):',
        '1. Noise Resistance Test.',
        '2. .',
        '',
        '>> Experiment setup:',
        'source: smartphone --bluetooth--> speaker',
        'volume: max * 0.1',
        'signal_type: white noise',
        'signal_frequency_hz: N/A',
        'sampling_rate_hz: 16000',
        'h_distance_cm: 10',
        'v_distance_cm: -3 (on table)',
        'run: 1',
        '',
        '>> Parameter',
        'samp_dp = {0}'.format(samp_dp),
        'samp_ds = {0}'.format(samp_ds),
        'chunk =   {0}'.format(chunk),
        'alpha =   {0}'.format(alpha),
        '',
        '>> Figure:',
        'content: power estimation result of each individual channel',
        'x-axis: samples',
        'y-axis: Watt',
        'title: the channel facing the audio source',
        'legend: final power estimation value of each channel',
        '',
        '>> Result: ({0})'.format(now),
    ]
    with open(fp + fn, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
    print('Initiated experiment summary report')


if __name__ == '__main__':
    ep, esfn = init_directory(path_select=2)
    init_sumfile(100, 100, 100, 0.1, ep, esfn)
