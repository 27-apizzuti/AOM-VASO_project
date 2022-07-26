# -*- coding: utf-8 -*-

"""Prepare condition order, targets and noise texture for stim presentation."""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
import numpy as np
import os



runs = 1

    
# %% set parameters
NumOfCond = 1  # Number of different conditions [ originally there were 3: Right, Center and Left; currently Center is used]
NumRepCond = 27 # Number of repetitions per condition per run
NrOfTargets = 20  # Number of targets that participants need to detect

 
StimDur = 10  # Dur moving dots, in TRs
IsiDur = np.array([10]) ##np.array([6, 8, 10])  # jitter Dur ISI
FixDur = 10  # Dur fixation in beginning and end

    
for runID in runs:

    # %% define conditions
    conditions = []
    for ind in range(0, NumRepCond):
        CondOrder = np.arange(1, NumOfCond+1)
        np.random.shuffle(CondOrder)
        BaseOrder = np.zeros(NumOfCond, dtype=np.int)
        block_elem = np.insert(BaseOrder, np.arange(len(CondOrder)), CondOrder)
        conditions = np.hstack((conditions, block_elem))
       
    # if Right and Left conditions were used: 
    # Pos = np.where(conditions == 2)
    # conditions[Pos] = 1
    # Pos = np.where(conditions ==3)
    # conditions[Pos] =1
    
    # add -1 in beginning and end, for fixation dot
    conditions = np.hstack(([-1], conditions))
    # make sure array is int
    conditions = conditions.astype(int)
    
    
    # %% define durations of stimulus and rest
    durations = np.ones(len(conditions), dtype=np.int)*StimDur
    # tile IsiDur so it matches the NumRepCond
    if NumRepCond % len(IsiDur) != 0:
        print('WARNING: NumRepCond not exact multiples of IsiDur')
        IsiDur = np.tile(IsiDur, int(NumRepCond/len(IsiDur)))
    
    for ind in CondOrder:
        Pos = np.where(conditions == ind)[0]+1
        np.random.shuffle(IsiDur)
        durations[Pos] = IsiDur
    Pos = np.where(conditions == -1)
    durations[Pos] = FixDur  # Dur fixation
    
    conditions[Pos] = 0 #for prt saving and stim presentation
    
    # %% define the target onsets
    
    # prepare random target positions
    
    lgcRep = True
    while lgcRep:
       
        targets = np.random.choice(np.arange(FixDur, np.sum(durations)-FixDur),
                                   NrOfTargets, replace=False)
        # check that two Targets do not follow each other immediately
        lgcRep = np.greater(np.sum(np.diff(np.sort(targets)) <= 1), 0)
    
    targets = np.sort(targets)
    
    # %% save the results
    
    str_path_parent_up = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))
    filename = os.path.join(str_path_parent_up, 'Conditions',
                            'MtLoc_AOM_run0' + str(runID))
    
    np.savez(filename, Conditions=conditions, Durations=durations, Targets=targets)
