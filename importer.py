#region Import Modules

import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np

#endregion

#region Functions

def import_pico_log(pico_filepath, varnames=None):
    df = pd.read_csv(pico_filepath, index_col=None)
    df = df.rename(columns=varnames)

    for i, col in df.iterrows():
        df.loc[i, 't_absolute'] = datetime.datetime.strptime(df.loc[i, 't_absolute'], "%Y-%m-%dT%H:%M:%S%z")

    return df

def import_can_log(can_filepath,hour_start,minute_start,second_start, year_start=datetime.datetime.now().year,\
                   month_start=datetime.datetime.now().month, day_start=datetime.datetime.now().day,\
                   tz=datetime.timezone(datetime.timedelta(seconds=3600))):

    t_abs_0 = datetime.datetime(year_start, month_start, day_start, hour_start, minute_start, second_start, tzinfo=tz)
    df = pd.read_csv(can_filepath, index_col=None, delimiter=';')


    df = df.interpolate(method='nearest')
    df['t_relative'] /= 1000
    df['Fan_speed']*=100

    for i, col in df.iterrows():
        df.loc[i, 't_absolute'] = t_abs_0 + datetime.timedelta(seconds=df.loc[i, 't_relative'])

    return df


#endregion

#region Import Pico

root_path='C:/Users/JoãoGonçaloCouto/I-Charging\Miguel Sousa - Dimensionamento Controlo/'
folder_path='T_ref_50_T_heatsink_83'
pico_filename='pico.csv'
pico_dict_names={
    'Unnamed: 0' : 't_absolute',
    'AMBIENT_TEMPERATURE Ave. (C)' : 'T_amb',
    'TOUT Ave. (C)' : 'T_out',
    'POWERCELL_ELETRONICS_OUTPUT Ave. (C)' : 'T_pce_out',
    'TIN Ave. (C)' : 'T_in',
    'POWERCELL_POWER_OUTPUT Ave. (C)' : 'T_pcp_out',
    'PSU_FANS Ave. (C)' : 'T_psu_fans',
    'BOARDS Ave. (C)' : 'T_boards',
    'HEATSINK_DIODE Ave. (C)' : 'T_heatsink',
    'PSU_Retractor Ave. (C)' : 'T_psu_retractor',
    'PSU_HMI Ave. (C)' : 'T_psu_hmi',
    'PSU_ELETRONICS Ave. (C)' : 'T_psu_eletronics',
    'POWERCELL_POWER_INPUT Ave. (C)' : 'T_pcp_in',
    'POWERCELL_ELETRONICS_INPUT Ave. (C)' : 'T_pce_in',
    'DISPLAY_INPUT Ave. (C)' : 'T_hmi_in',
    'DISPLAY_OUTPUT Ave. (C)' : 'T_hmi_out',
    'DIODE_OUTPUT Ave. (C)' : 'T_diode_out',
}
pico_filepath=root_path+folder_path+'/'+pico_filename

df=import_pico_log(pico_filepath,varnames=pico_dict_names)

#endregion

#region Import CAN

can_filename='can.csv'
can_filepath=root_path+folder_path+'/'+can_filename

year=2020
month=10
day=19
hour=16
minute=6
second=47


df2=import_can_log(can_filepath,hour,minute,second, year_start=year, month_start=month, day_start=day)

#endregion

#region Synchronization

df1_dt=df.set_index('t_absolute')
df2_dt=df2.set_index('t_absolute')

DF_dt=pd.concat([df1_dt,df2_dt])
DF_dt['t_relative']=(DF_dt.index.values-DF_dt.index.values[0])

DF_dt['t_relative']=DF_dt['t_relative']/np.timedelta64(1, 's')

DF_dt['P_charger']=DF_dt['I_charger']*DF_dt['V_charger']/1000


#endregion

#region Export to Feather

DF2=DF_dt.reset_index()
DF2.to_feather(root_path+folder_path+'/'+'dataframe')


#endregion
