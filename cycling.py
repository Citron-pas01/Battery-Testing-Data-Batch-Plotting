# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:59:50 2021

@author: bfn5081
"""

import csv
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

styles = ['-','-','-','-','-','-','-','-','--', '--','--','--','--','--', '--', '--','-.','-.','-.','-.','-.','-.',\
   '-.',':']
Colr = ['black','black','blue','blue','green', 'green', 'purple', 'purple', 'yellow', 'yellow', 
        'orange','orange','magenta','magenta','red','red','gray','gray','lime', 'lime','gold', 
        'gold', 'cyan', 'cyan', 'pink','pink','skyblue','skyblue','teal', 'teal','olive', 'olive',
        'slategray','slategray','peru', 'peru','tomato','tomato','darkgoldenrod','darkgoldenrod',
        'maroon','maroon','darkorchid','darkorchid','indigo','indigo','navy','navy']

markers = ['o', 's']

def cycling_curve(x,y,filename,curve_label):
    lines = []
    fig = plt.figure(filename)
    ax = fig.add_subplot()
    ax.set_xlabel('Capacity (mAh)')
    ax.set_ylabel('Voltage (V)')             ###
    mpl.rc("font", family="Times New Roman",weight='normal')
    plt.rcParams.update({'mathtext.default':  'regular' })
    for i in range(len(x)):
        #print(len(x))
        lines += ax.plot(x[i], y[i], styles[1],color=Colr[i])

    test = '[%s]'%', '.join(map(str,curve_label))
    ax.annotate(test, xy=(0.65, 0.9), xycoords='axes fraction', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8),
                horizontalalignment='left', verticalalignment='bottom')
    ax.legend(fontsize='7', ncol=len(x),handleheight=0.8, labelspacing=0.03, \
                    loc='lower center',bbox_to_anchor=(0.5, -0.5), frameon=False)
    ax.set_title(filename+ ':' + 'Discharge-charge curves') 
    fig.savefig(filename+'Graph1.png')


def data_process(filepath, filename, end_cycle):
    data = pd.read_csv(filepath)
    search_1 = ['NaN','Cycle','Record']
    
    # only retain the cycle data and remove all the records in each step 
    cycle_stat_pre = data[~data['Cycle'].str.contains('|'.join(search_1))]
    cycle_stat = cycle_stat_pre.dropna() # drop rows with NaN

    # select rows which are with NaN values in 'Efficiency' column
    cycle_data = cycle_stat_pre[cycle_stat_pre['Efficiency/%'].isna()]

    cycle_data = cycle_data.iloc[:,:5].rename(columns={'Cycle':'Record',
                                                       'CapD/mAh':'Current/mA', 
                                                       'SpeCapC/mAh/g': 'Capacity/mAh', 
                                                       'SpeCapD/mAh/g': 'Voltage/V'})

    zero_current = ['0.00','0.000','0.0000']
    cycle_data = cycle_data[~cycle_data['Current/mA'].str.contains('|'.join(zero_current),na=False)]

    # transform current column into numeric array
    x = cycle_data['Current/mA'].values.tolist()
    x = list(map(float, x))
    
    # get out the row indexes where switching charge into discharge, vicevera
    index = []
    for i in range(len(x)):
        if x[i]*x[i-1]<0:
            index.append(i)
    #print(len(index))
 
    capacity = []
    voltage = []

    # if there are less than 5 cycles: 1st : length
    # [5, 10): 1st, 2nd, 5th
    # [10, 50): 1st, 2nd, 5th, 10th
    # [50, 100): 1st, 2nd, 5th, 10th, 50th
    # [100, 500), 1st, 2nd, 5th, 10th, 50th, 100th
    if end_cycle < 5:
        cycle_selection = range(0,len(index))
        curve_label = ['1st','2nd','3rd', '4th','5th'][:end_cycle]
        
    elif 5 <= end_cycle < 10:
        cycle_selection = [0,1, 2,3, 8,9]
        curve_label = ['1st','2nd','5th']

    elif 10 <= end_cycle < 50:
        cycle_selection = [0,1, 2,3, 8,9, 18,19]
        curve_label = ['1st','2nd','5th','10th']

    elif 50 <= end_cycle < 100:
        cycle_selection = [0,1, 2,3, 8,9, 18,19, 48,49]
        curve_label = ['1st','2nd','5th','10th','50th']

    elif 100 <= end_cycle < 500:
        cycle_selection = [0,1, 2,3, 8,9, 18,19, 48,49, 98,99]
        curve_label = ['1st','2nd','5th','10th','50th','100th']

    else:
        cycle_selection = [0,1, 2,3, 8,9, 18,19, 48,49, 98,99, 498,499]
        curve_label = ['1st','2nd','5th','10th','50th','100th','500th']
        
    for i in cycle_selection:
        start = 0
        if i ==0 and index[0] !=0:
            start = 0
        elif i>0:
            start = index[i-1]

        capacity_i = cycle_data['Capacity/mAh'].iloc[start:index[i]].values.tolist()
        voltage_i = cycle_data['Voltage/V'].iloc[start:index[i]].values.tolist()
        
        capacity.append(list(map(float, capacity_i)))
        voltage.append(list(map(float, voltage_i)))
    


    cycling_curve(capacity,voltage,filename,curve_label)

    print('ICE:{}; reversible CE: {} '.format(cycle_stat.iloc[0,-1], cycle_stat.iloc[:,-1].max()))
    #print(cycle_stat)
    return cycle_stat


def cycle_stat(dict,end_cycle):

    # correlate the sample name and the cyclic properties
    sample_name = []
    data_set = []
    for k, p in dict.items():
        sample_name.append(k)
        data_set.append(p)

    # set the cycle number steps
    if end_cycle <= 10:
        steps = end_cycle
    elif 10< end_cycle <= 50:
        steps = int(end_cycle/5)
    elif 50 < end_cycle <= 100:
        steps = int(end_cycle/10)
    elif 100 < end_cycle <= 200:
        steps = int(end_cycle/20)
    else:
        steps = int(end_cycle/50)

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Cycle Number')
    ax1.set_xticks(np.linspace(1, end_cycle, num=steps))
    ax1.set_ylabel('Specific Capacity (mAh/g)', color='tab:red')             
    mpl.rc("font", family="Times New Roman",weight='normal')
    plt.rcParams.update({'mathtext.default':  'regular' })

    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_yticks(np.linspace(0, 2000, num=9))
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Coulombic Efficiency (%)', color='tab:blue')  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_yticks([x for x in range(0, 110,10)])

    for i in range(len(dict)):
        color = Colr[2*i]
        #print(sample_name[i])

        x = list(map(int, data_set[i]['Cycle'].values.tolist()))

        y1 = list(map(float, data_set[i]['SpeCapD/mAh/g'].values.tolist()))

        y2 = list(map(float, data_set[i]['Efficiency/%'].values.tolist()))

        ax1.scatter(x, y1, s=14, c=color, marker=markers[0], label=sample_name[i])
        ax1.plot(x, y1, c=color )
    
        ax2.scatter(x, y2, s=14, color=color,facecolors='none', marker=markers[1])
        ax2.plot(x, y2, c=color )


    ax1.legend(fontsize='7', ncol=4,handleheight=0.8, labelspacing=0.03, \
                    loc='center',bbox_to_anchor=(0.6, 0.5), frameon=False)
    ax1.set_title('Cyclic Scatters') 
    fig.savefig( 'cyclic figure.png')
    fig.tight_layout()
    plt.show()


