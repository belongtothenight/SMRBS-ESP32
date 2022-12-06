from alg import PE
import pandas as pd
import os
pd.reset_option('display.float_format')


def run(export_path, ch_id):
    # set parameters
    runs = 100
    chunk = 300

    # run alg.py
    pe = PE(chunk_=chunk, img_path_=export_path)
    pe.continuous_run(runs, plot=False)
    pe.evaluate()

    # extract data
    lpe11 = []
    lpe12 = []
    lpe13 = []
    lpe14 = []
    lpe15 = []
    lpe16 = []
    for i in range(runs):
        lpe11.append(pe.mem_pe11[i][-1])
        lpe12.append(pe.mem_pe12[i][-1])
        lpe13.append(pe.mem_pe13[i][-1])
        lpe14.append(pe.mem_pe14[i][-1])
        lpe15.append(pe.mem_pe15[i][-1])
        lpe16.append(pe.mem_pe16[i][-1])
    data = {
        'max_ch': pe.mem_max_ch,
        'pe11': lpe11,
        'pe12': lpe12,
        'pe13': lpe13,
        'pe14': lpe14,
        'pe15': lpe15,
        'pe16': lpe16,
        'pe11avg': pe.mem_pe11avg,
        'pe12avg': pe.mem_pe12avg,
        'pe13avg': pe.mem_pe13avg,
        'pe14avg': pe.mem_pe14avg,
        'pe15avg': pe.mem_pe15avg,
        'pe16avg': pe.mem_pe16avg,
    }

    # export csv
    print()
    df = pd.DataFrame(data)
    csv_path = os.path.join(export_path, 'fair_comparison_ch{0}.csv'.format(ch_id))
    df.to_csv(csv_path, index=False)
    print(df.shape)

    # print summary
    stats = df.describe()
    stats.drop(['max_ch'], axis=1, inplace=True)
    csv_path = os.path.join(export_path, 'fair_comparison_stats_ch{0}.csv'.format(ch_id))
    stats.to_csv(csv_path)
    print(stats.shape)

    # export txt
    txt_path = os.path.join(export_path, 'fair_comparison_summary.txt')
    with open(txt_path, 'a') as f:
        for x in pe.mem_evaluation:
            for y in x:
                f.write(y + '\n')

    pe.terminate()


if __name__ == '__main__':
    # get folder name
    while True:
        subfolder = 'fc' + input('Enter subfolder count in fc (int): ')
        dir = os.path.join(os.getcwd(), 'fair_comparison', subfolder)
        if os.path.exists(dir):
            break
        else:
            print('Folder does not exist. Try again.')

    while True:
        ch_id = input('Enter run id (int), \'q\' to quit: ')
        if ch_id == 'q':
            break
        else:
            run(dir, ch_id)
