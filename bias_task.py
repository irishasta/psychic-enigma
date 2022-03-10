#Coded January 22
#Behavioral ratings for model fMRI study 
#----------------------------------------------------------------
#Experiment description: Valence ratings of music clips for pilot
#----------------------------------------------------------------
import os
import serial
import sys
import numpy as np
import pandas as pd
import psychopy.gui
import psychopy.visual
import psychopy.event
import psychopy.core
from psychopy import data, logging, sound, prefs
from psychopy.constants import *  # things like STARTED, FINISHED
from random import randint
from random import shuffle
import random
import time
import re
#----select sound library----
if prefs.general['audioLib'][0] == 'pyo':
    sound.init(48000,buffer=128)
print sound.audioLib

#----Get subject ID----
gui = psychopy.gui.Dlg() #adds text
gui.addField("Subject ID:") #adds labelled input field to dialogue box
gui.show() #shows box
subj_id = gui.data[0]
print subj_id #troubleshoot
#
#----Create file path for rating data, valence and arousal in separate files----
data_path = "data/subject"+str(subj_id)+"_bias.csv";
while os.path.exists(data_path): #if path exists, rename it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj_id+"000"
    data_path = "data/subject"+str(subj_id)+"_bias.csv"
#
#----Declare experiment variables
#Read in list of stim from csv file 
#----Read in pre-specified pseudorandom order of conditions----
items=pd.read_csv("trial_list.csv", header=None);  #
trial_list = items[0];
print trial_list
shuffle(trial_list);
#

#valence question/response
valence_question = "Do you think the expression is positive or negative?"
valence_resp_line1 = "positive = [9]         negative = [0]"
question_pos=350; #position of rating question

n_trials=21; #Total number of trials
n_vars=3;   #Number of fields (3): trial#, stim_id, rating)
X=np.zeros((n_trials,n_vars));   #Create blank vector to store data
#
#----Open experiment window
win = psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=False, #change to true when you run a subject
    color=[0, 0, 0]
)
#
#----Declare image and text variables
welcome_text = psychopy.visual.TextStim(
    win=win,
    text="Press any key to begin...",
    color=[1, 1, 1],
    height=35
)
#
fixation_img = psychopy.visual.ImageStim(
    win=win,
    image="fixation.jpg",
    units="pix"
    )
finish_text = psychopy.visual.TextStim(
    win=win,
    text="Please ring the bell.",
    color=[1, 1, 1],
    height=35,
    wrapWidth=1000
)

#Display waiting screen
welcome_text.draw()
win.flip()
psychopy.event.waitKeys()

#---------------------------------------------------------
#----Begin Experimental Trials------------------------------------
#---------------------------------------------------------
question = valence_question;
resp_line1 = valence_resp_line1;
print question
question_text = psychopy.visual.TextStim(
    win=win,
    text=question,
    color=[1, 1, 1],
    pos=(0,question_pos),
    alignHoriz='center',
    height=30,
    wrapWidth=1200
        )
resp1_text = psychopy.visual.TextStim(
    win=win,
    text=resp_line1,
    color=[1, 1, 1],
    pos=(0,-question_pos+59),
    alignHoriz='center',
    height=30,
    wrapWidth=1200
)
#--------Begin picture loop
trial_counter=0;
for i in range(0,n_trials):
    #First display fixation for 2 secs
    fixation_img.draw()
    win.flip() #start with fixation
    psychopy.core.wait(2) #wait two seconds
    #Define path to trial stimulus
    filename = "stim/bias_task/"+trial_list[i];
    #Draw stim
    img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix",
        pos=(0,0.5)
    )
    size_x = img.size[0]
    size_y = img.size[1]
    img.size = [size_x*0.7, size_y*0.7]   #scale image
    img.draw()
    question_text.draw()
    resp1_text.draw()
    win.flip()
    #Collect response----
    keys = psychopy.event.waitKeys(keyList=["9","0"]) #what keys they press
    stim_id = re.findall('\d+', filename)
    X[i,0] = i;
    X[i,1] = int(stim_id[0]);
    X[i,2] = keys[0][0];
    print X[i]
#---------------------------------------------------------
#----Save the data----------------------------------------
#---------------------------------------------------------
np.savetxt(
    data_path,
    X,
    delimiter=",",
    header="Trial Number, Stim ID, Response"
)


#---------------------------------------------------------
#----Show finish screen-----------------------------------
#---------------------------------------------------------
finish_text.draw()
win.flip()
psychopy.event.waitKeys()
