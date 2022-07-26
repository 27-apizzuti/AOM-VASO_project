#!/usr/b2112in/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 17:46:10 2020

@author: amaiab
"""

from __future__ import absolute_import, division, print_function

from builtins import str
from psychopy import visual, event, core

#%%

win = visual.Window(fullscr=False)

globalClock = core.Clock()
counter = visual.TextStim(win, height=.05, pos=(0, 0), color=win.rgb + 0.5)
duration = 100

while globalClock.getTime() < duration:

    for keys in event.getKeys():
        if keys[0] in ['escape', 'q']:
            win.close()
            core.quit()
            
        else: 
                
            counter.setText("button " + str(kqeys[0]) + " was pressed")
            counter.draw()
            win.flip()

win.close()
core.quit()