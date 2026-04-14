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
red_patch=mpatches.Patch(color='red', label='< $1000')
orange_patch=mpatches.Patch(color='orange', label='$1000 - 3000')
blue_patch=mpatches.Patch(color='blue', label='> $3000')
ax.legend(handles=[red_patch,orange_patch,blue_patch])
plt.show()

timesY=[]
timesA=[]
timesS=[]
outcomeY=[]
outcomeA=[]
outcomeS=[]

for client in clients:
    wdf=dfinit.loc[dfinit['id_fix']==client]
    age=wdf['age_type'].dropna().unique()[0]
    #for each client, record the number of months they survived in the study. 
    time=(wdf['time'].max()-wdf['time'].min())/np.timedelta64(1, 'D')/30
    if age=="Young Adult":
        timesY.append(time)
    if age=="Middle Adult":
        timesA.append(time)
    if age=="Senior":
        timesS.append(time)
    #If they made it to december, record False. Otherwise, record true
    uncensored=True
    if wdf['time'].max().month==12:
        uncensored=False
    if age=="Young Adult":
        outcomeY.append(uncensored)
    if age=="Middle Adult":
        outcomeA.append(uncensored)
    if age=="Senior":
        outcomeS.append(uncensored)


datY=pd.DataFrame({'uncensored':outcomeY,'time':timesY,})
datA=pd.DataFrame({'uncensored':outcomeA,'time':timesA,})
datS=pd.DataFrame({'uncensored':outcomeS,'time':timesS,})

tY, spY, ciY = kaplan_meier_estimator(
    datY["uncensored"], datY["time"], conf_type="log-log"
)

tA, spA, ciA = kaplan_meier_estimator(
    datA["uncensored"], datA["time"], conf_type="log-log"
)

tS, spS, ciS = kaplan_meier_estimator(
    datS["uncensored"], datS["time"], conf_type="log-log"
)
fig, ax = plt.subplots()
low=ax.step(tY, spY, where="post",color="red")
ax.fill_between(tY, ciY[0], ciY[1], alpha=0.25, step="post",color="red")
middle=ax.step(tA, spA, where="post",color="orange")
ax.fill_between(tA, ciA[0], ciA[1], alpha=0.25, step="post",color="orange")
high=ax.step(tS, spS, where="post",color="blue")
ax.fill_between(tS, ciS[0], ciS[1], alpha=0.25, step="post",color="blue")
plt.ylim(0, 0.7)
plt.ylabel(r"est. probability of continued program use $\hat{S}(t)$")
plt.xlabel("time (months) $t$")
plt.title("Probability of Continued Use of the Food Pantry Program by Age Group")
red_patch=mpatches.Patch(color='red', label='Young Adult')
orange_patch=mpatches.Patch(color='orange', label='Middle Adult')
blue_patch=mpatches.Patch(color='blue', label='Senior')
ax.legend(handles=[red_patch,orange_patch,blue_patch])
plt.show()

dfinit['num_people']=dfinit['num_male']+dfinit['num_female']

people={}
x=0
for client in clients:
    wdf=dfinit.loc[dfinit['id_fix']==client]
    num_p=wdf['num_people'].dropna().unique()
    if num_p.size==0:
        num_p=1 #this accounts for instances where a client has no specified number of people
        x+=1
    people.setdefault(client, num_p)

dfinit['num_people']=dfinit['id_fix'].replace(people)
dfinit['month']=dfinit['time'].dt.month
#people per month
people=[]
month=[]
for m in range(12):
    s=dfinit['num_people'].loc[dfinit['month']==m+1].sum()
    people.append(s)
    month.append(m+1)
ppmdat=pd.DataFrame({'Month':month,'People':people,})
print(ppmdat['People'].median())
print(ppmdat)
sns.barplot(data=ppmdat,y='People',x='Month')
plt.title('Estimated People Assisted per Month')
plt.show()
print(ppmdat['People'].std())
print(ppmdat['People'].var())
print(x)