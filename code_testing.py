import numpy as np

rng = np.random.default_rng(42)
n = 10
pref_list = {}
ns = np.arange(1, n + 1)
for i in range(1, n + 1):
    print(rng.permutation(ns).tolist())
