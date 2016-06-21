import pandas as pd
import datetime
import numpy as np

df = pd.read_csv('storyline1.csv') #Load CSV file
print df
print "Number of Days sampled:", len(np.unique(df['Date']))
print df.Date.value_counts()

d0 = datetime.date(2014, 10, 19) #start date
d1 = datetime.date(2016, 6, 6) #end date
delta = d1 - d0
print delta.days #number of days where data was collected

#Create list of dates
dates = [] 
for x in range (0, 596): #upper bound should be delta.days
    dates.append(d0 + datetime.timedelta(days = x))

#Create a data frame out of start/stop time columns, extracting time info only
dates=np.asarray(dates)
df['Start'].apply(str)
df.Start = df.Start.astype(str)
startdf=df['Start'].str.split('T', expand=True)
enddf=df['End'].str.split('T', expand=True)
start_time_df=startdf[1].str.split('-', expand=True)
end_time_df=enddf[1].str.split('-', expand=True)
time_df=startdf[[0]],start_time_df[[0]],end_time_df[[0]]
time_df=pd.concat([startdf[[0]],start_time_df[[0]],end_time_df[[0]]], axis=1, keys=['date', 'start time', 'stop time'])
print time_df

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

#Convert 24-hour clock to seconds
for i in range(0, len(time_df)):
    time_df.ix[i,1]=get_sec(time_df.ix[i,1])
    time_df.ix[i,2]=get_sec(time_df.ix[i,2])

time_df['start time'] = time_df['start time'] + 1 #add 1 to all start times that say 0
time_df['stop time']=time_df['stop time'].replace(['0'], '86400') #convert all stop times that are 0 to 86400
print time_df


pd.set_option('display.max_columns', 4)
places=np.unique(df['Name'])
df['code'] = pd.Categorical.from_array(df.Name).codes #recode categorical "Names" column to numerical codes
a=df.Name.value_counts()
b=df.code.value_counts()

#Pad codes so all are three digits
df["padded code"] = ""
counter=0
for index in df.code:
    if len(str(index)) < 3:
        temp=(str(index))
        temp=temp.zfill(3)
        df.loc[counter, "padded code"]=temp
    elif len(str(index)) == 3:
        df.loc[counter, "padded code"]=index
    counter=counter+1
print df["padded code"]

#Create newdf to include in project
newdf=time_df.join(df["padded code"])
newdf.columns = ['Date', 'Start', 'End', 'Code']
print newdf

moves=np.zeros(shape=(delta.days,86400)) #create an empty array of 0s
moves=moves.astype(str)
counter=0
#Append correct code in place of 0's, remaining 0's mean that at that timepoint app was not collecting data
for i in range(0,len(time_df)):
    if str(dates[counter]) == str(time_df.ix[i, 'date']):
        col_start=int(time_df.ix[i,'start time'])
        col_end=int(time_df.ix[i,'stop time'])
        print df.ix[i, 'padded code']
        moves[counter,col_start:col_end]=df.ix[i, 'padded code']
        print moves[counter,col_start:col_end]
    else:
        counter=counter+1
print moves

#Checking to make sure right code appended to right cells
n=1
col_start=int(time_df.ix[n,'start time'])
col_end=int(time_df.ix[n,'stop time'])
print col_start, col_end, df.ix[n, 'padded code'], len(time_df)

#Downsample data- extracting every 30th second
prac=moves[:, 0::30]
prac[prac == '0.0'] = '000'
e = np.tile("end", prac.shape[0])[None].T
prac=np.hstack([prac,e])
print prac

#Save to txt file
import os
np.savetxt('test.txt', moves, fmt='%.5s', delimiter=' ', newline=os.linesep)



