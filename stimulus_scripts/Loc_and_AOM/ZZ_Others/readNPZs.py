#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:01:06 2020

@author: amaiab
"""


from pathlib import Path
import numpy as np
import pandas as pd
# import openpyxl
#%%

mainPath = Path("/Volumes/Elements/motion_quartet_data/motion_quartet_scripts-master/StimulusScripts/")
savingPath = mainPath / "Excel"
runType = ['RndDotMot','HukLocaliser']
fileNameCore = ['AOM', 'MtLoc_AOM']
NrOfRuns = [8,2]

for runTypeId in np.arange(0,len(runType)):
    
    data_folder = mainPath / runType[runTypeId] / "Conditions"
    runs = np.arange(1,NrOfRuns[runTypeId]+1) 
    d = {}
   
    if runTypeId ==0:
        filePath = savingPath / ("Output_" + str(fileNameCore[runTypeId]) + ".xlsx")
    else:
        filePath = savingPath / ("Output_" + str(fileNameCore[runTypeId]) + ".xlsx")
    for runId in runs:
    
        if runTypeId ==0:
            filename =  (fileNameCore[runTypeId] + "_run0" + str(runId) +  ".npz")
        else:
            filename =  (fileNameCore[runTypeId] + "_run0" + str(runId) +  ".npz")
            
        npzfile = np.load(data_folder / filename, allow_pickle=True, encoding = 'ASCII')
    
        Conditions = npzfile['Conditions']
        print(Conditions)
        
        # load durations of stimulus and rest
        Durations = npzfile['Durations']
        print(np.cumsum(Durations))
        
        # load the target onsets
        Targets = npzfile['Targets']
        print(Targets)
        
        A = (Conditions,
             np.cumsum(Durations))
        
        cDurations = np.cumsum(Durations)
        Conditions = Conditions
        Durations = Durations
        
        if runTypeId==0:
            Durations2 = Durations*2
            cDurations2 = np.cumsum(Durations2)
            data = np.transpose(np.asarray([Conditions,Durations,cDurations,Durations2,cDurations2]))       
            d[runId-1] = pd.DataFrame(data,index=None, columns=['Condition ID','Duration in TR1', 'Cumulative Duration in TR1', 'Duration in TRtot', 'Cumulative Duration in TRtot'])
        else:
            data = np.transpose(np.asarray([Conditions,Durations,cDurations]))       
            # d[runId-1] = pd.DataFrame(data,index=None, columns=['Condition ID','Duration in TR1', 'Cumulative Duration in TR1'])
            d[runId-1] = pd.DataFrame(data,index=None, columns=['Condition ID','Duration in TR1', 'Cumulative Duration in TR1'])

    # save dataframes to excel sheet
    counter = 0
    for df in runs:
        print(df)
        if (df)==1:
        # if df==1:
            with pd.ExcelWriter(filePath) as writer:
                d[df-1].to_excel(writer, sheet_name=("run0" + str(df)))
                # d[df-5].to_excel(writer, sheet_name=("run0" + str(df)))
        else:
            with pd.ExcelWriter(filePath,engine="openpyxl", mode='a') as writer:
                d[df-1].to_excel(writer, sheet_name=("run0" + str(df)))
                # d[df-5].to_excel(writer, sheet_name=("run0" + str(df)))
        counter=counter+1
            
