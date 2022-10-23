from alg import PE
import pandas as pd
pd.reset_option('display.float_format')

export_path = 'fair_comparison/'
runs = 5
chunk = 300

pe = PE(chunk_=chunk, img_path_=export_path)
pe.continuous_run(runs, plot=False)
pe.evaluate()

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
print()
df = pd.DataFrame(data)
df.to_csv(export_path + 'fair_comparison.csv', index=False)
print(df.shape)

stats = df.describe()
stats.drop(['max_ch'], axis=1, inplace=True)
stats.to_csv(export_path + 'fair_comparison_stats.csv')
print(stats.shape)

with open(export_path + 'fair_comparison_summary.txt', 'a') as f:
    for x in pe.mem_evaluate:
        for y in x:
            f.write(y + '\n')

pe.terminate()
