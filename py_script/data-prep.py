import imp
from msilib import add_data
import pandas as pd
import glob
import os

input_files = glob.glob("../datasets/ECU_DATA/2018*.csv", recursive=True)

all_data = None

for i in range(len(input_files)):
    csv_columns = []
    csv_columns.append('time')
    header_number = 0
    channel = ""
    with open(input_files[i]) as f:
        lines = f.readlines()
        for line in lines:
            header_number += 1
            if line.startswith('Channel : '):
                channel = line.replace('Channel : ','').replace('\n','')
            if line.startswith('Type : '):
                csv_columns.append(channel + "[" + line.replace('Type : ','').replace('\n','') + "]")
            if line.startswith('Log : '):
                break
    print("{} header={}  file={}".format(i+1, header_number, input_files[i]))
    df = pd.read_csv(input_files[i], index_col=False, skiprows=header_number, names=csv_columns)
    
    basename = os.path.basename(input_files[i])
    df['date'] = basename.replace('.csv','').split('-')[0]
    route = basename.replace('.csv','').split('-')[1]
    df['route'] = route
    df['time'] = df['date'] + " " + df['time']
    df['time'] = pd.to_datetime( df['time'], format="%Y%m%d %H:%M:%S.%f")
    df['#time_diff'] = df['time'].diff(1).dt.total_seconds()
    df['#time_seq'] = df['#time_diff'].cumsum()
    df['#road_seq'] = df['#time_seq']
    if route == "mimos2home":
        df['#road_seq'] = df['#road_seq'].max() - df['#road_seq']

    if all_data is None:
        all_data = df
    else:
        all_data = pd.concat([all_data, df])


# all_data.dropna(inplace=True)

print(all_data.head())

