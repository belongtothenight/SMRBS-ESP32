from alg import PE
from alg_report import init_sumfile
import datetime
import os


def init_directory():
    while True:
        exp_num = input(
            'Enter pe_comparison.py experiment run number: (number, \'q\' to quit) ')
        export_path = '/home/pi/SMRBS-ESP32/algorithm/pe_comparison/run{0}/'.format(
            exp_num)
        export_summary_fn = 'summary.txt'
        if exp_num == 'q':
            exit()
        elif os.path.exists(export_path):
            print('Folder already exist, delete it or give it a different number.')
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


if __name__ == '__main__':
    # set parameters
    ep, esfn = init_directory()

    # run alg.py
    chunk = 1000
    pe = PE(chunk_=chunk)
    samp_dp = pe.samp_dp
    samp_ds = pe.samp_ds
    chunk = pe.chunk
    alpha = pe.alpha
    i = -1
    ch = []
    export_lines = {1: '', 2: '', 3: '', 4: '', 5: '', 6: ''}
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
                           fn=ep)
            print('Exported plots to {0}'.format(ep))
            # export lines
            init_sumfile(samp_dp, samp_ds, chunk, alpha,
                         ep, esfn)
            with open(ep + esfn, 'a', encoding='utf-8') as f:
                for j in range(len(export_lines)):
                    f.write(export_lines[j+1])
            pe.clear_data()
            i = -1
            ch = []
            print('Exported lines to {0}'.format(ep))
        else:
            num = int(num)
            ch.append(num)
            while True:
                pe.read_data()
                pe.pow()
                if pe.pe1():
                    continue
                else:
                    break
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
