""" 
Multiple types of daily actions and falls are contained in each file (csv) of the MMsys (Cognet) dataset.
Here the acceleration data are distinguished into separate sets according to the labels and seperately are send to the fall detection function.
"""

import time
import math
import pandas as pd

from def_fall import fall_detection


def extract_ranges(lst):
    extracted_list = []
    previous_value = None

    for value in lst:
        if value != previous_value:
            extracted_list.append(value)
        previous_value = value
    
    return extracted_list

def check_dataset(df, file):

    timestamp = []
    
    length = 0
    counter = 0
    counter2 = 0
    
    clas = []
    pre = []
    
    x1 = []
    y1 = []
    z1 = []
    v1 = [] 
        
    g = 9.807
    
    for i in (range(len(df))):
        
        """ Use the data from cheist """
        x1.append(df.ch_accel_x[i]*g)
        y1.append(df.ch_accel_y[i]*g)
        z1.append(df.ch_accel_z[i]*g)
        
        """ Use the data from thigh """
        # x1.append(df.th_accel_x[i]*g)
        # y1.append(df.th_accel_y[i]*g)
        # z1.append(df.th_accel_z[i]*g)
        

    current_time = time.time()
    timestamp.append(current_time)
    
    """ Generate the timestamps """
    for i in (range(len(df))):
        current_time += 0.01
        timestamp.append(current_time)  
    
    """ Calculate the magnitudes """
    for i in (range(len(x1))):
        v1.append(math.sqrt(math.pow(x1[i],2) + math.pow(y1[i],2) + math.pow(z1[i],2) ))
    
    """ Save the labels to a list """
    annot1 = df.annotation_2.to_list()    
    
    v2 = []
    v3 = []
    timestamp2 = []
    timestamp3 = []
    pre_anot = annot1[0]
    v2.append(v1[0])
    
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    for i in range(len(v1)):
         
        """ Create a set of magnitudes which correspond to an action based to the labels/annoattions """
        if annot1[i] == pre_anot:
            v2.append(v1[i])
            timestamp2.append(timestamp[i])
            
        else:
            
            """ Create the data-frame that contains the magnitudes and the correspond timestamps and it will be send to the function that applies the fall detection task """
            df2 = pd.DataFrame(list(zip(v2, timestamp2)),
                           columns =['v', 'time'])
            
            
            """ In the falls-variable are saved the total falls which have been detected """
            """ Τhe function arguments are the aforementioned data-frame, the length of the time-series, and the frequency of the sensor """
            falls = len(fall_detection(df2,len(df2), hz=100))
            
            """ Send the magnitudes which are NOT correspond to the last action of the file """ 
            if annot1[i-1] != 0:
                
                counter2+=1
                
                flag_fall = False
                
                """ Labels which correspond to a fall """
                if annot1[i-1] == 2 or annot1[i-1] == 6 or annot1[i-1] == 10 or annot1[i-1] == 11 or annot1[i-1] == 12 or annot1[i-1] == 13:
                    flag_fall = True
                else:
                    length = length + len(v2)
                    counter+=1
                
                """ Calculate if the detection is TP, FP(s), TN and FN according to the annotations and the detection results """
                if flag_fall:
                    if falls == 1:
                        tp+=1
                    elif falls == 0:
                        fn+=1
                    elif falls > 1:
                        tp+=1
                        fp+=(falls-1)
                    else:
                        print('error')
                else:
                    if falls == 0:
                        tn+=1
                    elif falls != 0:
                        fp+=falls
                    else:
                        print('error')
                        
                
                clas.append(annot1[i-1])
                pre.append(falls)
                    
                            
            v2 = []
            timestamp2 = []
            v2.append(v1[i])
            timestamp2.append(timestamp[i])
         
        """ Send the magnitudes which are correspond to the last action of the file """ 
        if i == len(v1) - 1:
            print(file)
            df2 = pd.DataFrame(list(zip(v2, timestamp2)),
                           columns =['v', 'time'])
            
            """ In the falls-variable are saved the total falls which have been detected """
            """ Τhe function arguments are the aforementioned data-frame, the length of the time-series, and the frequency of the sensor """            
            falls = len(fall_detection(df2,len(df2), hz=100))
            
            if annot1[i-1] != 0:
                
                counter2+=1
                
                flag_fall = False
                
                """ Labels which correspond to a fall """
                if annot1[i-1] == 2 or annot1[i-1] == 6 or annot1[i-1] == 10 or annot1[i-1] == 11 or annot1[i-1] == 12 or annot1[i-1] == 13:
                    flag_fall = True
                else:
                    length = length + len(v2)
                    counter+=1
                
                """ Calculate if the detection is TP, FP(s), TN and FN according to the annotations and the detection results """
                if flag_fall:
                    if falls == 1:
                        tp+=1
                    elif falls == 0:
                        fn+=1
                    elif falls > 1:
                        tp+=1
                        fp+=(falls-1)
                    else:
                        print('error')
                else:
                    if falls == 0:
                        tn+=1
                    elif falls != 0:
                        fp+=falls
                    else:
                        print('error')
                        
                clas.append(annot1[i-1])
                pre.append(falls)
        
        pre_anot = annot1[i]
    
    """ The csv files, which correspond to an action with the label 15, are contained by continiously actions """
    """ The subject is continuously ascending/descending a staircase and we split each action to be consists of 1500 acceleration data """
    if len(v2) == (len(v1)+1):
        
        for i in range(len(v2)):
                     
            v3.append(v2[i])
            timestamp3.append(timestamp[i])
            
            if len(v3) % 1500 == 0:
                
                counter2+=1
                
                df3 = pd.DataFrame(list(zip(v3, timestamp3)),
                               columns =['v', 'time'])
                
                """ In the falls-variable are saved the total falls which have been detected """
                """ Τhe function arguments are the aforementioned data-frame, the length of the time-series, and the frequency of the sensor """                
                falls = len(fall_detection(df3,len(df3), hz=100))
                
                """ Calculate if the detection is TP, FP(s), TN and FN according to the annotations and the detection results """
                if falls == 0:
                    tn+=1
                elif falls != 0:
                    fp+=falls
                else:
                    print('error')
                
                clas.append(15)
                pre.append(falls)
                
                v3 = []
                timestamp3 = []
    
    """ Return the TPs, FFs, TNs and FNs of the CSV that contains multiple types af daily actions and falls """
    return tp, fp, tn, fn