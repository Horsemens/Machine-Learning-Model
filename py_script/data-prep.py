from msilib import add_data
import shutil
import pandas as pd
import glob
import os
import sys 

input_files = glob.glob("../datasets/ECU_DATA/2018*.csv", recursive=True)
CLEAN_DATA_DIR_PATH = "../clean_data/"
ECU_DATA_DIR_PATH = CLEAN_DATA_DIR_PATH +"/ECU_DATA"
if(os.path.exists(CLEAN_DATA_DIR_PATH)):
    shutil.rmtree(CLEAN_DATA_DIR_PATH)

if(os.path.exists("../all-data.csv")):
    os.remove("../all-data.csv")

os.makedirs(ECU_DATA_DIR_PATH)
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
    # df['date'] = basename.replace('.csv','').split('-')[0]
    # route = basename.replace('.csv','').split('-')[1]
    # df['route'] = route
    # df['time'] = df['date'] + " " + df['time']
    # df['time'] = pd.to_datetime( df['time'], format="%Y%m%d %H:%M:%S.%f")
    # df['#time_diff'] = df['time'].diff(1).dt.total_seconds()
    # df['#time_seq'] = df['#time_diff'].cumsum()
    # df['#road_seq'] = df['#time_seq']
    # if route == "mimos2home":
    #     df['#road_seq'] = df['#road_seq'].max() - df['#road_seq']

    
    df1 = df.iloc[:]
    df2 = df.iloc[:]
    dfnew = df

    drop_columns = [
        "TransientThrottlePercentageEnrich[Percentage]",
        "TransientThrottlePercentageAsync[Percentage]",
        "TransientThrottleEnrichDecayRate[msPerEngCyl]",
        "TransientThrottleEnrichSensitivity[Time_us]",
        "TransientThrottleAccelCoolantCorr[Percentage]",
        "ShiftLight1[Raw]",
        "FuelCoolantTempCorrection[Percentage1For1]",
        "FuelAirTempCorrection[Percentage]",
        "IgnitionLoad[Pressure]",
        "TargetAFR[AFR]",
        "ThrottlePosition[Percentage]",
        "time",
        "CurrentDutyCycle[Percentage]",
        "Load[Pressure]",
    ]

    if "Unnamed: 0" in  list(df.columns):
        drop_columns.append("Unnamed: 0")

    if "Pwm_State_1[Raw]" in  list(df.columns):
        drop_columns.append("Pwm_State_1[Raw]")
    
    if "Pwm_State_2[Raw]" in  list(df.columns):
        drop_columns.append("Pwm_State_2[Raw]")
    
    dfnew.drop(drop_columns,axis=1,inplace=True)
    dfnew['sno'] = range(1, 1+len(dfnew))
    cols = dfnew.columns.delete(len(dfnew.columns)-1)
    cols = list(cols)
    cols.insert(0, "sno")
    dfnew = dfnew[cols]
    dfnew = dfnew.ffill()
    dfnew.to_csv("../clean_data/{}".format(input_files[i].split("/")[-1]))
    if all_data is None:
        all_data = dfnew
    else:
        all_data = pd.concat([all_data, dfnew])


# if(len(sys.argv) > 1):
#     try:
#         rows = int(sys.argv[1])
#     except:
#         rows = 10000

# all_data = all_data[:rows]
all_data.to_csv("../all-data.csv")
