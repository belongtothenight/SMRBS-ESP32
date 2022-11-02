from alg import PE
chunk = 500
pe = PE(chunk_=chunk)
i = -1
ch = []
while True:
    num = input(
        '\nEnter number of testing channel: (\'q\' to quit and export plots) ')
    i += 1
    if num == 'q':
        break
    ch.append(num)
    pe.read_data()
    pe.pow()
    pe.pe1()
    pe.dc1()
    pe.store_data()
for j in range(i):
    pe.plt_pe1(maxch=ch[j], fi=j, fn='/home/pi/code_alg/pe_comparison/')
pe.terminate()
del pe
print('Finished executing!')
