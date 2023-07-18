import os
from tqdm import tqdm
import pandas as pd

from m_analyse_1_csv_in_def_2 import check_dataset

""" 
Multiple types of daily actions and falls are contained in each file (csv) of the MMsys (Cognet) dataset.
"""
  
path = "path to the folder that contains the csb from the MMsys (Cognet) dataset"

files2 = os.listdir(path)
files = []

for file in tqdm(files2):
    
    if file.split('.')[1] == 'csv':
        files.append(file)

tp = 0
fp = 0
tn = 0
fn = 0

tp_1 = []
fp_1 = []
tn_1 = []
fn_1 = []
name = []

for file in tqdm(files):
    
    if file.split('.')[1] == 'csv':
        df = pd.read_csv(os.path.join(path,file))
        
        """ Each CSV that contains multiple action is sent to the check_dataset function to seperate each sub-action. """ 
        """ While are returned the TPs, FPs,TNs and FNs which have found. """ 
        tp_0, fp_0, tn_0, fn_0 = check_dataset(df, file)
                
        tp_1.append(tp_0)
        fp_1.append(fp_0)
        tn_1.append(tn_0)
        fn_1.append(fn_0)
        name.append(file)
        
        tp+=tp_0
        fp+=fp_0
        tn+=tn_0
        fn+=fn_0


acc  = (tp + tn) / (tp + fp + tn + fn)
prec = tp/(tp+fp)
sens = tp/(tp+fn)
rec = sens
spec = tn/(tn+fp)
f1 = 2*(rec*prec)/(rec+prec)

index2 = []
for n in name:
    
    index2.append(int(n.split('_')[1].split('.')[0]))
    
    
results = pd.DataFrame(list(zip(name, tp_1, fp_1, tn_1, fn_1, index2)),
               columns =['file', 'TP', 'FP', 'TN', 'FN', 'index2'])  
results = results.sort_values(by='index2')
# results.to_csv('results.csv')

print("\nAcc: {:.4f}\nSen: {:.4f}\nSpe: {:.4f}\nPre: {:.4f}\nF1 : {:.4f}".format(acc, sens, spec, prec, f1))
