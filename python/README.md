Here the fall detection algorithm is implemented in the Python programming language.

The function in line 54 performs the task of fall detection.
As arguments should be given a data-frame (df2) that contains in the column v the magnitudes and in the column time the corresponding timestamps, 
the length (step2) of the time-series (data-frame) and 
the frequency (Hz) of the sensor that is used.

The two other .py files (m_analyse_1_csv_in_def_2.py and m_analyse_all_csvs.py) are given for testing the algorithm in the MMsys (Cognet) dataset [1].
To test the algorithm on the aforementioned dataset that contains acceleration data on multiple types of daily actions and falls, please follow these steps:

1. Download the MMsys dataset from http://skuld.cs.umass.edu/traces/mmsys/2015/paper-15/ and save all the csv files (subject_x.csv) to a path (only the csvs).
2. Give the path to the line 11 of m_analyse_all_csvs.py
3. Install the following python libraries:
    pip3 install pandas /
    pip3 install numpy /
    pip3 install tqdm /
4. Save all the three .py files in the same folder
5. If you want uncomment the line 69 of the m_analyse_all_csvs.py to save a csv file (results.csv) that will contain all the TPs, FPs, TNs and FNs for each subject_x.csv .
6. run the m_analyse_all_csvs.py (python3 m_analyse_all_csvs.py). Upon completion, the console will display the accuracy, sensitivity, specificity, precision, and F1 score.

[1] Ojetola, O.; Gaura, E.; Brusey, J. Data Set for Fall Events and Daily Activities from Inertial Sensors. In Proceedings of the Proceedings of the 6th ACM multimedia systems conference, 2015, pp. 243–248
