from alg import PE

pe = PE(chunk_=300)
pe.continuous_run(5, plot=False)
pe.evaluate()
pe.terminate()
