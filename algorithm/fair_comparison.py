from alg import PE
import pandas as pd

runs = 1000
pe = PE(chunk_=300, img_path_='fair_comparison')
pe.continuous_run(runs, plot=False)
pe.evaluate()

lpe11 = []
lpe12 = []
lpe13 = []
lpe14 = []
lpe15 = []
lpe16 = []
for i in range(runs):
    lpe11.append(pe.pe11[i][-1])
    lpe12.append(pe.pe12[i][-1])
    lpe13.append(pe.pe13[i][-1])
    lpe14.append(pe.pe14[i][-1])
    lpe15.append(pe.pe15[i][-1])
    lpe16.append(pe.pe16[i][-1])
data = {
    'p1avg': pe.p1avg,
    'p2avg': pe.p2avg,
    'p3avg': pe.p3avg,
    'p4avg': pe.p4avg,
    'p5avg': pe.p5avg,
    'p6avg': pe.p6avg,
    'pe11avg': pe.pe11avg,
    'pe12avg': pe.pe12avg,
    'pe13avg': pe.pe13avg,
    'pe14avg': pe.pe14avg,
    'pe15avg': pe.pe15avg,
    'pe16avg': pe.pe16avg,
    'pe11': lpe11,
    'pe12': lpe12,
    'pe13': lpe13,
    'pe14': lpe14,
    'pe15': lpe15,
    'pe16': lpe16,
}
df = pd.DataFrame(data)
df.head()


pe.terminate()
