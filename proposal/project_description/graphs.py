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

#%% Data obtained from Open Library Textbooks (see file open-textbook-library.py)

math = {"count": 119, "formats": {"PDF": 118, "HTML": 47, "Hardcopy": 43, "LaTeX": 21, "eBook": 16, "MS Word": 4, "XML": 3}, "licenses": {"CC BY-NC-SA": 38, "CC BY-SA": 29, "Free Documentation License (GNU)": 9, "CC BY-NC": 10, "CC BY": 28, "CC BY-NC-ND": 3, "CC0": 1, "CC BY-ND": 1}}
sciences = {"count": 145, "formats": {"HTML": 83, "eBook": 57, "PDF": 142, "XML": 26, "ODF": 16, "MS Word": 6, "Hardcopy": 30, "Google Doc": 1, "LaTeX": 1}, "licenses": {"CC BY-SA": 10, "CC BY-NC-SA": 55, "CC BY": 49, "CC BY-NC": 24, "CC BY-NC-ND": 7}}
engineering = {"count": 39, "formats": {"HTML": 14, "eBook": 12, "PDF": 38, "XML": 6, "Hardcopy": 15, "LaTeX": 1, "ODF": 6, "MS Word": 2}, "licenses": {"CC BY": 8, "CC BY-NC": 10, "CC BY-NC-SA": 14, "CC BY-SA": 4, "Free Documentation License (GNU)": 3}}
cs = {"count": 35, "formats": {"PDF": 35, "Hardcopy": 10, "eBook": 11, "HTML": 18, "MS Word": 2, "XML": 1, "LaTeX": 5}, "licenses": {"CC BY-SA": 4, "CC BY-NC": 7, "CC BY-NC-SA": 17, "CC BY": 7}}

open_books = {
    'mathematics': math,
    'natural sciences': sciences,
    'engineering': engineering,
    'computer science': cs,    
    }


#%% Combine Google Doc, MS Word and XML with ODF
for disc, topic in open_books.items():
    
    topic['formats']['XML/ODF'] = 0
    topic['formats']['Word/Google'] = 0
    
    for f, v in topic['formats'].items():
        
        if f == 'ODF' or f == 'XML':
            topic['formats']['XML/ODF'] += v
            
        if f == 'MS Word' or f == 'Google Doc':
            topic['formats']['Word/Google'] += v
            
    
    if 'XML' in topic['formats']:
        del topic['formats']['XML']
    if 'ODF' in topic['formats']:
        del topic['formats']['ODF']
    if 'MS Word' in topic['formats']:
        del topic['formats']['MS Word']
    if 'Google Doc' in topic['formats']:
        del topic['formats']['Google Doc']
            
#%%
discs = list(open_books.keys())

open_books['stem'] = {'count': 0, 'formats': {}}

for name in discs:
    topic = open_books[name]
    
    open_books['stem']['count'] += topic['count']
    
    for f, v in topic['formats'].items():
        open_books['stem']['formats'][f] = open_books['stem']['formats'].get(f, 0) + v

#%%
all_formats = []
for disc in open_books.values():
    all_formats += disc['formats'].keys()
    
all_formats = list(set(all_formats))

all_formats = sorted(all_formats, key=lambda x: open_books['stem']['formats'][x], reverse=True)    

#%%
fs = 24
fw = 'bold'

for name in open_books:
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    topic = open_books[name]
    
    data = dict([(f, 0) for f in all_formats])
        
    for f, v in topic['formats'].items():
        data[f] = round(v / topic['count'] * 100)
        
    count = topic['count']
    
    values = list(data.values())
        
    formats = list(data.keys())
    
    x_pos = np.arange(1, len(values) + 1)
    
    ax.bar(x_pos, values, color='gray', edgecolor='black')
    
    ax.set_ylabel('\nPercent [\%]', 
                  fontsize=fs, fontweight=fw)
    
    title = name.upper() if name == 'stem' else name.title()
    
    ax.set_title(f'\n{title} Textbooks Formats ({count})\n', fontsize=fs, fontweight=fw)
    ax.set_ylim(0, max(values) + 10)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(formats, fontsize=16, fontweight=fw, rotation=45)
    
    for k, v in enumerate(values):
        ax.text(x_pos[k] - 0.25, v + 3, f'{v}\%', fontsize=round(fs*0.75), fontweight=fw)

    
    fig.savefig(f'{name}-textbook-formats.png', dpi=200, transparent=True)


#%% Formats for all STEM disciplines







