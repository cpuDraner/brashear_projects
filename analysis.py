from brashear_projects.readers import brashread
import seaborn as sns
import pandas as pd
from sksurv.nonparametric import kaplan_meier_estimator
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

dfinit=brashread.PantryDat('C:/sockdrawer/brashear_projects/data/pantry_data.xlsx').df
dat=False
clients=dfinit['id_fix'].unique()
uncensoreds=[]
times=[]
for client in clients:
    wdf=dfinit.loc[dfinit['id_fix']==client]
    #for each client, record the number of months they survived in the study. 
    time=(wdf['time'].max()-wdf['time'].min())/np.timedelta64(1, 'D')/30
    times.append(time)
    #If they made it to december, record False. Otherwise, record true
    uncensored=True
    if wdf['time'].max().month==12:
        uncensored=False
    uncensoreds.append(uncensored)

dat=pd.DataFrame({'uncensored':uncensoreds,'time':times})

t, sp, ci = kaplan_meier_estimator(
    dat["uncensored"], dat["time"], conf_type="log-log"
)
plt.step(t, sp, where="post",color="blue")
plt.fill_between(t, ci[0], ci[1], alpha=0.25, step="post")
plt.ylim(0, 0.6)
plt.ylabel(r"est. probability of continued program use $\hat{S}(t)$")
plt.xlabel("time (months) $t$")
plt.title("Probability of Continued Use of the Food Pantry Program")
plt.show()
        

timesL=[]
timesM=[]
timesH=[]
outcomeL=[]
outcomeM=[]
outcomeH=[]

for client in clients:
    wdf=dfinit.loc[dfinit['id_fix']==client]
    income=wdf['income_type'].dropna().unique()[0]
    #for each client, record the number of months they survived in the study. 
    time=(wdf['time'].max()-wdf['time'].min())/np.timedelta64(1, 'D')/30
    if income=="Low":
        timesL.append(time)
    if income=="Medium":
        timesM.append(time)
    if income=="High":
        timesH.append(time)
    #If they made it to december, record False. Otherwise, record true
    uncensored=True
    if wdf['time'].max().month==12:
        uncensored=False
    if income=="Low":
        outcomeL.append(uncensored)
    if income=="Medium":
        outcomeM.append(uncensored)
    if income=="High":
        outcomeH.append(uncensored)


datL=pd.DataFrame({'uncensored':outcomeL,'time':timesL,})
datM=pd.DataFrame({'uncensored':outcomeM,'time':timesM,})
datH=pd.DataFrame({'uncensored':outcomeH,'time':timesH,})

tL, spL, ciL = kaplan_meier_estimator(
    datL["uncensored"], datL["time"], conf_type="log-log"
)

tM, spM, ciM = kaplan_meier_estimator(
    datM["uncensored"], datM["time"], conf_type="log-log"
)

tH, spH, ciH = kaplan_meier_estimator(
    datH["uncensored"], datH["time"], conf_type="log-log"
)
fig, ax = plt.subplots()
low=ax.step(tL, spL, where="post",color="red")
ax.fill_between(tL, ciL[0], ciL[1], alpha=0.25, step="post",color="red")
middle=ax.step(tM, spM, where="post",color="orange")
ax.fill_between(tM, ciM[0], ciM[1], alpha=0.25, step="post",color="orange")
high=ax.step(tH, spH, where="post",color="blue")
ax.fill_between(tH, ciH[0], ciH[1], alpha=0.25, step="post",color="blue")
plt.ylim(0, 0.6)
plt.ylabel(r"est. probability of continued program use $\hat{S}(t)$")
plt.xlabel("time (months) $t$")
plt.title("Probability of Continued Use of the Food Pantry Program by Income Level")
red_patch=mpatches.Patch(color='red', label='Low')
orange_patch=mpatches.Patch(color='orange', label='Medium')
blue_patch=mpatches.Patch(color='blue', label='High')
ax.legend(handles=[red_patch,orange_patch,blue_patch])
plt.show()