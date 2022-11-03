from alg import PE
chunk = 500
pe = PE(chunk_=chunk)
i = -1
ch = []
while True:
    num = input(
        '\nEnter number of testing channel: (\'q\' to quit, \'e\' export plots) ')
    i += 1
    if num == 'q':
        break
    elif num == 'e':
        for j in range(i):
            pe.plt_pe1(maxch=ch[j], fi=j,
                       fn='/home/pi/code_alg/pe_comparison/')
        pe.clear_data()
        i = -1
        ch = []
    else:
        ch.append(num)
        pe.read_data()
        pe.pow()
        pe.pe1()
        pe.dc1()
        pe.store_data()
pe.terminate()
del pe
print('Finished executing!')
