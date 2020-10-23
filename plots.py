import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

root_path='C:/Users/JoãoGonçaloCouto/I-Charging\Miguel Sousa - teste_dentro_camara/'
folder_path='T30\PWM20'
DF_dt=pd.read_feather(root_path+folder_path+'/'+'dataframe')

PWM='Control'
P_charger=50
T_amb=40

fig=plt.figure(figsize=(8,4))
fig.suptitle('T_amb = '+str(T_amb)+'[°C]'+' | '+'Charger Power ='+str(P_charger)+'[kW]'+' | '+' | '+'PWM = '+str(PWM)+' [%] ')
grid = plt.GridSpec(2, 5, wspace=0.4, hspace=0.3)
ax=[]
ax.append(
    plt.subplot(grid[1,:3])
)

smoothing_period=1000


ax[0].plot(DF_dt['t_relative'],DF_dt['P_charger'], label='P_charger - [kW]',linestyle='--')
ax[0].plot(DF_dt['t_relative'],DF_dt['DeltaP_fan_in'].rolling(window=smoothing_period).median(),label='DeltaP_fan_in - [Pa]')
ax[0].plot(DF_dt['t_relative'],DF_dt['PWM'],label='PWM - [%]',linestyle=':')

#ax[0].set_ylim([0,250])
ax[0].legend()
ax[0].set_ylabel('Power | Pressure | Duty Cycle - [kW] | [Pa] | [%]')
ax[0].set_xlabel('Elapsed time - [s]')




ax.append(
    plt.subplot(grid[1,3:],sharex=ax[0])
)
ax[1].plot(DF_dt['t_relative'],DF_dt['Fan_speed'].rolling(window=smoothing_period).median(), label='Fan Speed - [rpm]')

ax[1].legend()
ax[1].set_ylim([0,10000])
ax[1].set_ylabel('Frequency - [rpm]')
ax[1].set_xlabel('Elapsed time - [s]')

ax.append(
    plt.subplot(grid[0,0],sharex=ax[0])
)

ax[2].plot(DF_dt['t_relative'],DF_dt['T_in'],label='T_in')
ax[2].plot(DF_dt['t_relative'],DF_dt['T_out'],label='T_out')
#ax[2].plot(DF_dt['t_relative'], DF_dt['T_amb'],label='T_amb')

ax[2].legend()

ax.append(
    plt.subplot(grid[0,1],sharex=ax[0])
)

ax[3].plot(DF_dt['t_relative'],DF_dt['T_pce_in'],label='T_pce_in')
ax[3].plot(DF_dt['t_relative'],DF_dt['T_pce_out'],label='T_pce_out')
ax[3].plot(DF_dt['t_relative'], DF_dt['T_pcp_in'],label='T_pcp_in')
ax[3].plot(DF_dt['t_relative'],DF_dt['T_pcp_out'],label='T_pcp_out')

ax[3].legend()


ax.append(
    plt.subplot(grid[0,2],sharex=ax[0])
)

ax[4].plot(DF_dt['t_relative'],DF_dt['T_psu_fans'],label='Fans')
ax[4].plot(DF_dt['t_relative'],DF_dt['T_psu_retractor'],label='Retractor')
ax[4].plot(DF_dt['t_relative'], DF_dt['T_psu_eletronics'],label='Eletronics')
ax[4].plot(DF_dt['t_relative'],DF_dt['T_psu_hmi'],label='HMI')

ax[4].legend()


ax.append(
    plt.subplot(grid[0,3],sharex=ax[0])
)

ax[5].plot(DF_dt['t_relative'],DF_dt['T_hmi_in'],label='Inlet')
ax[5].plot(DF_dt['t_relative'],DF_dt['T_hmi_out'],label='Outlet')

ax[5].legend()

ax.append(
    plt.subplot(grid[0,4],sharex=ax[0])
)

ax[6].plot(DF_dt['t_relative'],DF_dt['T_heatsink'],label='Heatsink - Interior')
ax[6].plot(DF_dt['t_relative'],DF_dt['T_diode_out'],label='Heatsink - Medium Outlet')
ax[6].plot(DF_dt['t_relative'],DF_dt['T_pcp_out'],label='PCP_OUT')

ax[6].legend()