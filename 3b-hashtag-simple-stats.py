import sys
import pandas as pd
import numpy as np
from scipy import stats
from operator import itemgetter
import time

df = pd.read_pickle("tweets.pkl")
df = df.drop_duplicates(subset="id_str")

ht_2_freq = {}

for i in range(0, df.shape[0]):
    ht1 = df.iloc[i]["entities"]["hashtags"]
    if(len(ht1) > 0):
        for j in range(0, len(ht1)):
            ht2 = (ht1[0]["text"])
            if (ht2 in ht_2_freq.keys()):
                ht_2_freq[ht2] += 1
            else:
                ht_2_freq[ht2] = 1

ht_2_freq_sorted = sorted(ht_2_freq.items(), key = itemgetter(1), reverse = True)
top = ht_2_freq_sorted[0:10]
ht = [i[0] for i in top]
freq = [i[1] for i in top]

for i in range(0, len(ht)):
    print(ht[i], "("+str(freq[i])+")")
