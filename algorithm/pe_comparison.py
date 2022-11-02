from alg import PE
chunk = 500

while True:
    num = input('\nEnter number of testing channel: (\'q\' to quit) ')
    if num == 'q':
        break
    pe = PE(chunk_=chunk)
    pe.read_data()
    pe.pow()
    pe.pe1()
    pe.dc1()
    pe.store_data()
    pe.plt_pe1(maxch=num)
    pe.terminate()
    del pe
