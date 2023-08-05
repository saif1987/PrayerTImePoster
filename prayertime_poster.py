# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 17:51:59 2023

@author: Saifuddin
"""

#pip install geopy
#pip install prayertime
#pip install timezonefinder
from geopy.geocoders import Nominatim as Nm 
import prayertime_custom as pt
import datetime, pytz
import pandas as pd
import numpy as np

# =============================================================================
# import plotly.io as pio
# import plotly.express as px
# pio.renderers.default='browser'
# =============================================================================
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


geoloc=Nm(user_agent='test')
loc=geoloc.geocode('peoria')
cal=pt.Calendar.IslamicSocietyOfNorthAmerica
maz=pt.Mazhab.Default
season=pt.Season.Winter #default


# =============================================================================
# mypt=pt.Prayertime(loc.longitude, loc.latitude, -5, 2023, 7, 30, pt.Calendar.IslamicSocietyOfNorthAmerica, pt.Mazhab.Default,0 )    
# mypt.calculate()
# mypt.report()
# =============================================================================

#iterate over all days

columnnames=['date','tzUTC','fajr','shrouk',
             'zuhr',
             'asr','maghrib','isha']
mylist=np.zeros(shape=[0,len(columnnames)]);
local_timezone='US/Central'
year=2023
dt = datetime.datetime(year, 1, 1)
while dt.year == year:
    utcoffset = pytz.timezone('US/Central').localize(dt).utcoffset().total_seconds()/3600
    dt=dt + datetime.timedelta(days=1)
    mypt=pt.Prayertime(loc.longitude, loc.latitude, utcoffset, dt.year, dt.month, dt.day, cal, maz,season )
    mypt.calculate()
    
    

    fajr= datetime.datetime.strptime(mypt.fajr_time(),'%I:%M:%S %p')
    shrouk= datetime.datetime.strptime(mypt.shrouk_time(),'%I:%M:%S %p')
    
    zuhrsp = mypt.zuhr_time().replace(' ',':').split(':')
    if zuhrsp[0] == '0':
       zuhrtxt =  str('12:'+zuhrsp[1]+':'+zuhrsp[2]+' '+zuhrsp[3])
       print(zuhrtxt)
       zuhr = datetime.datetime.strptime(zuhrtxt,'%I:%M:%S %p') 
    elif (int(zuhrsp[0]) < 6 or int(zuhrsp[0]) ==12 ) and zuhrsp[3] == 'AM':
        zuhrtxt =  str(zuhrsp[0]+':'+zuhrsp[1]+':'+zuhrsp[2]+' '+'PM')
        print(zuhrtxt)
        zuhr = datetime.datetime.strptime(zuhrtxt,'%I:%M:%S %p')
    elif int(zuhrsp[0]) > 6 and int(zuhrsp[0])<12 and zuhrsp[3] == 'PM':
        zuhrtxt =  str(zuhrsp[0]+':'+zuhrsp[1]+':'+zuhrsp[2]+' '+'AM')
        print(zuhrtxt)
        zuhr = datetime.datetime.strptime(zuhrtxt,'%I:%M:%S %p')  
    else:
        zuhr = datetime.datetime.strptime(mypt.zuhr_time(),'%I:%M:%S %p')
    asr= datetime.datetime.strptime(mypt.asr_time(),'%I:%M:%S %p')
    maghrib = datetime.datetime.strptime(mypt.maghrib_time(),'%I:%M:%S %p')
    isha = datetime.datetime.strptime(mypt.isha_time(),'%I:%M:%S %p')

    mylist=np.vstack([mylist,[dt,#.strftime('%m-%d-%Y'),
                              utcoffset,
                              fajr,
                              shrouk,
                              zuhr,
                              asr,
                              maghrib,
                              isha
                              ]])
    
print(dt.year)

df = pd.DataFrame(mylist,columns=columnnames)

plt.figure(1)

ax=plt.gca()
#ax.format_xdata= mdates.DateFormatter('%Y-%M-%D')
#ax.format_ydata= mdates.DateFormatter('%I:%M %p')
df.plot(x='date',y='fajr',ax=ax)
df.plot(x='date',y='shrouk',ax=ax)
df.plot(x='date',y='zuhr',ax=ax)
df.plot(x='date',y='asr',ax=ax)
df.plot(x='date',y='maghrib',ax=ax)
df.plot(x='date',y='isha',ax=ax)
ax.yaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))

# fig1=px.line(df,x='date',y='fajr',title='Fajr in Peoria')

#plt.figure(2)
# fig2=px.line(df,x='date',y='tzUTC',title='TimeZone in Peoria')