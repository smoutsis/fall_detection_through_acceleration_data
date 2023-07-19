Here the fall detection algorithm is implemented in the C++ programming language.

The funciton in line 131 (def_fall.cpp) performs the task of fall detection. As arguments shoulb be given a data class as defined in lines 15-24 of the header file (def_fall.hpp), 
the length (step2) of the time-series 
and the frequency (Hz) of the sensor that is used.

The kfall_paradigm.cpp file is given for testing a single csv file from the kfall dataset [1]. To test the algorithm on the aforementioned dataset please follow these steps:

1. Request access and downlowd the kfall dataset (sensor_data.zip) from https://sites.google.com/view/kfalldataset/
2. Enter the file path of the csv you want to test as a string in line 16 of kfall_paradigm.cpp
3. Download the following custom header library: rapidcsv.h (or using vcpkg : vcpkg install rapidcsv) -> https://github.com/d99kris/rapidcsv
4. Have all three files in the same directory or using a code editor in the same workplace, the console will display the number of falls which have been detected.

[1] Yu, X.; Jang, J.; Xiong, S. A Large-Scale Open Motion Dataset (KFall) and Benchmark Algorithms for Detecting Pre-impact Fall of the Elderly Using Wearable Inertial Sensors. Frontiers in Aging Neuroscience 2021, 13, 692865. 
