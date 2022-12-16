#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:00:02 2022

@author: cesar
"""

import numpy as np
import matplotlib.pyplot as plt

#%% Awareness of OER increase
oer_awareness = {
    '2014-15': 17,
    '2015-16': 22,
    '2016-17': 25,
    '2017-18': 28,
    '2018-19': 31,
    '2019-20': 37,
    '2021-22': 46}

fs = 24
fw = 'bold'
fig, ax = plt.subplots(figsize=(10, 10))

values = list(oer_awareness.values())
years = list (oer_awareness.keys())

x_pos = np.arange(1, len(values) + 1)

ax.bar(x_pos, values, color='gray', edgecolor='black')

ax.set_ylabel('\nPercent [\%]', 
              fontsize=fs, fontweight=fw)
# ax.set_xlabel('\nAcademic Year\n', fontsize=fs, fontweight=fw)
ax.set_title('\nFaculty Awareness of OER and CC by Year\n', fontsize=fs, fontweight=fw)
ax.set_ylim(0, 55)

ax.set_xticks(x_pos)
ax.set_xticklabels(years, fontsize=16, fontweight=fw, rotation=45)

for k, v in enumerate(values):
    ax.text(x_pos[k] - 0.2, v + 2, f'{v}\%', fontsize=fs, fontweight=fw)

fig.savefig('oer_awareness.png', dpi=200, transparent=True)