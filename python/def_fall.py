import pandas as pd
import numpy as np

""" Delete the indexes of the list1 which are given to list2 """  
def delete_items_by_indexes(list1, list2):
    new_list = [item for i, item in enumerate(list1) if i not in list2]
    return new_list

def max2(x,y):
    if x>y:
        return x
    else:
        return y

def max3(li):
    if len(li) == 0:
        return 0
    else:
        return max(li)

""" A list of lists are sent to the find_lists_with_same_number function that calculate if there are double connections """         
def find_lists_with_same_number(lst):
    number_indexes_0 = {}
    number_indexes_1 = {}
    
    for i, sublist in enumerate(lst):
        number_0, number_1 = sublist
        
        if number_0 in number_indexes_0:
            number_indexes_0[number_0].append(i)
        else:
            number_indexes_0[number_0] = [i]
        if number_1 in number_indexes_1:
            number_indexes_1[number_1].append(i)
        else:
            number_indexes_1[number_1] = [i]
    
    result_0 = [indexes for indexes in number_indexes_0.values() if len(indexes) > 1]
    result_1 = [indexes for indexes in number_indexes_1.values() if len(indexes) > 1]
    
    return result_0, result_1

def Average(lst):
    try:
        return sum(lst) / len(lst)
    except:
        return 0

""" The fall_detections function apply the fall detection tast and takes as arguments
    a data-frame that conatins in the column v the magnitudes and in the column time 
    the corresponding timestamps, the length of the time-series (data-frame) and the
    frequency of the sensor that is used.
"""  
def fall_detection(df2, step2, hz):
    
    g = 9.807
    time = []
    v = []
    
    for i in range(len(df2)):
        
        time.append(df2.time[i])
        v.append(df2.v[i])
    
    """ Create the entries """
    entry = []
    entry.append(0)
    for i in range(1,len(time)):
        entry.append(((time[i]-time[i-1])/10)+entry[i-1]+100/hz)
        
    df = pd.DataFrame(list(zip(entry, v)),
                   columns =['entry', 'v'])
    
    """ Calculate the average score of magnitudes """
    v_avg = Average((df.v).tolist())
    
    """ Set the Lists """
    low = []
    high = []
    new_low = []
    new_high = []
    
    fall = []
    index = []
    new_fall = []
    new_index = []
    
    new_fall2 = []
    new_index2 = []
    
    """ Make a list with the magnitides """
    v2 = (df.v).tolist()
    """ Make a list with the entries """
    entries = (df.entry).tolist()
    
    """ Evaluated Thresholds """
    min_limit = 6.5
    max_limit = max(v_avg,20)+ 10
    fall_duration = 105
    
    fall_limitation = 85
    max_limit_2 = max_limit
    
    """ Not Evaluated Thresholds """
    sub_1 = 50
    dist_1 = 100
    dist_2 = 100
    
    """ Find lows and highs """
    for i in range(len(df)):   
        if df.v[i] < min_limit:
            low.append(i)
        elif df.v[i] > max_limit:
            high.append(i)
    
    if len(high) == 0 or len(low) == 0:
        # print('No Fall')
        return(new_low)
    else:
        new_low = []
        new_high = []
        new_low.append(low[0])
        new_high.append(high[0])
        
        """ Create the sets of lows """
        for i in range(1,len(low)):
            
            if df.entry[low[i]] - df.entry[low[i-1]] > sub_1:
            # if df.entry[low[i]] - df.entry[low[i-1]] > 5 and df.entry[low[i]] - df.entry[low[i-1]] < 250:
                new_low.append(low[i-1])
                new_low.append(low[i])
            
            elif i == len(low)-1:
                new_low.append(low[i])
        
        if len(new_low)%2 == 1:
            new_low.append(new_low[len(new_low)-1])
        
        """ Create the sets of highs """
        for i in range(1,len(high)):
            
            if df.entry[high[i]] - df.entry[high[i-1]] > sub_1:
                new_high.append(high[i-1])
                new_high.append(high[i])
            
            elif i == len(high)-1:
                new_high.append(high[i])
        
        if len(new_high)%2 == 1:
            new_high.append(new_high[len(new_high)-1])
                       
        if len(new_high) == 0 or len(new_low) == 0:
            # print('No Fall')
            return(new_fall)
        else:
            track = 0
            
            """ Make the connection of lows and highs which correspond to falls """
            for i in range(0,len(new_low),2):

                for j in range(track,len(new_high),2):
                   
                    if (df.entry[new_high[j+1]] - df.entry[new_low[i]] < fall_duration) and (df.entry[new_high[j+1]] - df.entry[new_low[i]] > 0):
                        
                        fall.append([df.entry[new_low[i]], df.entry[new_high[j+1]]])
                        index.append([new_low[i], new_high[j+1]])
                        
                    elif (df.entry[new_high[j+1]] - df.entry[new_low[i+1]] < fall_duration) and (df.entry[new_high[j+1]] - df.entry[new_low[i+1]] > 0):

                        fall.append([df.entry[new_low[i+1]], df.entry[new_high[j+1]]])
                        index.append([new_low[i+1], new_high[j+1]])
                        
                    elif (df.entry[new_high[j]] - df.entry[new_low[i]] < fall_duration) and (df.entry[new_high[j]] - df.entry[new_low[i]] > 0):

                        fall.append([df.entry[new_low[i]], df.entry[new_high[j]]])
                        index.append([new_low[i], new_high[j]])
                        
                    elif (df.entry[new_high[j]] - df.entry[new_low[i+1]] < fall_duration) and (df.entry[new_high[j]] - df.entry[new_low[i+1]] > 0):

                        fall.append([df.entry[new_low[i+1]], df.entry[new_high[j]]])
                        index.append([new_low[i+1], new_high[j]])
                        
            
            new_index = index.copy()
            new_fall = fall.copy()
            indexes_to_del = []
                      
            if len(fall) == 0:
                # print('No Fall')
                return(new_fall)
            else:
                
                """ Find the double connections of lows """
                same_num_indexes = find_lists_with_same_number(fall)
                if len(same_num_indexes[0])!=0:
                    
                    for i in range(len(same_num_indexes[0])):
                        
                        for j in range(1,len(same_num_indexes[0][i]),1):
                            
                            sub1 = abs(fall[same_num_indexes[0][i][j-1]][0] - fall[same_num_indexes[0][i][j-1]][1])
                            sub2 = abs(fall[same_num_indexes[0][i][j]][0] - fall[same_num_indexes[0][i][j]][1])
                            
                            if sub1<sub2:
                                indexes_to_del.append(same_num_indexes[0][i][j])
                            else:
                                indexes_to_del.append(same_num_indexes[0][i][j-1]) 
                
                """ Find the double connections of highs """
                if len(same_num_indexes[1])!=0:
                    
                    for i in range(len(same_num_indexes[1])):
                        
                        for j in range(1,len(same_num_indexes[1][i]),1):
                            
                            sub1 = abs(fall[same_num_indexes[1][i][j-1]][0] - fall[same_num_indexes[1][i][j-1]][1])
                            sub2 = abs(fall[same_num_indexes[1][i][j]][0] - fall[same_num_indexes[1][i][j]][1])
                            
                            if sub1<sub2:
                                indexes_to_del.append(same_num_indexes[1][i][j])
                            else:
                                indexes_to_del.append(same_num_indexes[1][i][j-1]) 
                                
            """ Delete the longer double connection and keep the shorter """ 
            if len(indexes_to_del)!=0:
                new_index = delete_items_by_indexes(new_index, indexes_to_del)
                new_fall = delete_items_by_indexes(new_fall, indexes_to_del) 

            
            """ If the fall is long search if there are more lows close to the high and trasport the start of the fall to a closer low (Check 1) """
            for i in range(len(new_index)):
                
                if abs(new_fall[i][1]-new_fall[i][0]) > fall_limitation:
                    
                    for j in range(new_index[i][0], new_index[i][1], 1):
                        
                        if v2[j] < min_limit and  ((new_index[i][1] - j) > 5):

                            indexx = j
                    
                    if indexx != new_index[i][0]:
                        new_index[i][0] = indexx
                        new_fall[i][0] = entries[indexx]
                    
            """ Regect the fall if it is long (Check 2) """   
            for i in range(len(new_fall)):
                # if True:
                if abs(abs(new_fall[i][0]) - abs(new_fall[i][1])) < fall_limitation:
                    new_fall2.append(new_fall[i])
                    new_index2.append(new_index[i])
                else:
                    pass

            new_fall = new_fall2.copy()
            new_index = new_index2.copy()
            
            new_index_3 = []
            new_fall_3 = []
            v_after_fall = []
            
            """ Keep the fall either if the peak is the highest magnitude or the magnitudes after the fall are close to g (Check 3) """ 
            for i in range(len(new_index)):
                
                max_v = 0
                for j in range(new_index[i][0]-1,new_index[i][1]+1):
                    if v2[j] > max_v:
                        max_v = v2[j]
                        # indexx = j
                        
                t1 = new_fall[i][0]-1 - dist_1
                t2 = new_fall[i][1]+1 + dist_2
                
                j1 = None
                j2 = None
                
                for j in range(new_index[i][0]-1,0,-1):
                    
                    if new_fall[i][0] < t1:
                        j1 = j
                        break
                    else:
                        j1 = j

                for j in range(new_index[i][1]+1,len(v2),1):
                    
                    if new_fall[i][1] > t2:
                        j2 = j
                        break
                    else:
                        j2 = j

                if j1 == None:
                    j1 = 0
                
                if j2 == None:
                    j2 = len(v2)-1
                
                high_1_1 = []
                high_2_2 = []
                
                for j in range(j1,new_index[i][0]-1):
                    
                    if v2[j] > max_limit_2:
                        high_1_1.append(v2[j])
                        
                for j in range(new_index[i][1]+1,j2):
                    if abs(entry[j] - new_fall[i][1])>0.3:
                        v_after_fall.append(v2[j])
                    
                    if v2[j] > max_limit_2:
                        high_2_2.append(v2[j])
                        
                v_avg_after_fall = Average(v_after_fall)

                if ((v_avg_after_fall<g+2) and (v_avg_after_fall>g-2) and np.std(v_after_fall)<2 and len(v_after_fall)>20) or max_v>max2(max3(high_1_1),max3(high_2_2)):
                    new_index_3.append(new_index[i])
                    new_fall_3.append(new_fall[i])
                else:
                    pass
                
            new_fall = new_fall_3.copy()
            new_index = new_index_3.copy()   
            
            if len(new_fall) == 0:
                # print('No Fall')
                return new_fall
            else:
                return new_fall