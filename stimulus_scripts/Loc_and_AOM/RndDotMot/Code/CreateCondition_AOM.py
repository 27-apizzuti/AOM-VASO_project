# -*- coding: utf-8 -*-

"""Prepare condition order, targets and noise texture for stim presentation."""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
import numpy as np
import os

# %% set parameters

# set number of repetitions per condition per block
numRepCond = 2

# set # of TR1 of moving dot condition [this is half of the total TR]
durMot = 5 # 6
# set durations of baseline (jitter inter-stimulus interval)
if numRepCond == 3:
    durIsi = np.array([4,5,6])
elif numRepCond ==2:
    durIsi = np.array([5,6])
elif numRepCond ==1:
    durIsi = np.array([5])
    
# set duration of fixation in between blocks and end, in *TR1* units
durFix = 1 # defines end of block of aom [ in the middle of the run]
initFix = 5
# set target length
targetDur = 0.3  # in s
# set number of targets
nrOfTargets = 30 
# set directions
Directions = np.array([0, 45, 90, 135, 180, 225, 270, 315], dtype=np.int32)

runs = np.arange(1,9) # technically we only need one, since we are using the same run structure
# %% Create dictionary of parameters
dictParams = {}
dictParams['numRepCond'] = numRepCond
dictParams['durMot'] = durMot
dictParams['durIsi'] = durIsi
dictParams['durFix'] = durFix
dictParams['targetDur'] = targetDur
dictParams['nrOfTargets'] = nrOfTargets
dictParams['Directions'] = Directions

#%%
for runID in runs:
    
    print(runID)

    # %% define conditions
    Conditions = []
    for ind in range(0, numRepCond):
        CondOrder = np.arange(1, len(Directions)+1)
        np.random.shuffle(CondOrder)
        
        BaseOrder = np.zeros(len(Directions), dtype=np.int) # 0= static motion
    
        block_elem = np.insert(BaseOrder, np.arange(len(CondOrder)), CondOrder)
        #print(block_elem)
        # results in block_elem = [1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0]
        Conditions = np.hstack((Conditions, block_elem))
        #print(Conditions)
    # add -1 , -2 for different fixations throughout run
    insrtInd = np.linspace(0, len(Conditions), numRepCond+1, endpoint=True).astype(np.int32)
    Conditions = np.insert(Conditions, insrtInd[1:len(insrtInd)], [-1])
    Conditions = np.insert(Conditions, insrtInd[0], [-2])
    Conditions = Conditions.astype(np.int32)
    
    #%% check number of cond
    
    for ind in CondOrder:
        Pos = np.where(Conditions ==ind)[0]
        #print(len(Pos))
    
    Pos = np.where(Conditions == -1)[0]
    #print(len(Pos))
    # %% define durations of stimulus and rest
    Durations = np.ones(len(Conditions), dtype=np.int32)*durMot
    for ind in CondOrder:
        Pos = np.where(Conditions == ind)[0]+1
        durIsiElem = np.tile(durIsi, int(np.divide(len(Pos), len(durIsi))))
        np.random.shuffle(durIsiElem)
        Durations[Pos] = durIsiElem
    Pos = np.where(Conditions == -1)
    Durations[Pos] = durFix  # Dur fixation
    Pos = np.where(Conditions == -2)
    Durations[Pos] = initFix  # INITIAL fixation
    
    Durations = Durations.astype(np.int32)
    #print(sum(Durations)/60)
    
    # Make first item in condition = -1, for saving prt file later on
    Conditions[0] = -1
    # %% define the target onsets
    
    # prepare random target positions
    lgcRep = True
    # switch to avoid repetitions
    #while lgcRep:
    if initFix <=1:
         Targets = np.random.choice(np.arange(initFix+1, np.sum(Durations)-initFix),
                                   nrOfTargets, replace=False)
    else:    
        Targets = np.random.choice(np.arange(initFix, np.sum(Durations)-initFix),
                                   nrOfTargets, replace=False)
    # check that two Targets do not follow each other immediately
        #lgcRep = np.greater(np.sum(np.diff(np.sort(Targets)) <= 1), 0)
    Targets = np.sort(Targets)
    
    # %% save the results
    
    str_path_parent_up = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))
    filename = os.path.join(str_path_parent_up, 'Conditions',
                            ('AOM_run0' + str(runID)))
    
    np.savez(filename, Conditions=Conditions, Durations=Durations, Targets=Targets,
             dictParams=dictParams)
