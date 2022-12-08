import os
import numpy as np
import pandas as pd
os.system('cls')

path = 'fair_comparison_stats_mix.csv'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in lines]
lines = [line.replace(',', ' & ') for line in lines]

for line in lines:
    print(line)
