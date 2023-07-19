#include "def_fall.cpp"
#include "rapidcsv.h"
#include <string>
#include <iostream>
#include <chrono>

using namespace std::chrono;
using std::string;

int main(void)
{

    double maxx = 0;
    double minn = 100;

    string file = "Path to a csv file from the kfall dataset";

    /*Get accelaration data from the csv using the rapidcsv custom header library*/
    rapidcsv::Document doc(file);
    vector<double> AccX = doc.GetColumn<double>("AccX");
    vector<double> AccY = doc.GetColumn<double>("AccY");
    vector<double> AccZ = doc.GetColumn<double>("AccZ");

    vector<double> v = {};
    vector<double> timestamp = {};

    /*Create the total acceleration and timestamp vectors*/
    double current_time = duration_cast<seconds>(system_clock::now().time_since_epoch()).count();

    for (int i = 0; i < AccX.size(); i++)
    {
        v.push_back(sqrt(AccX[i] * AccX[i] + AccY[i] * AccY[i] + AccZ[i] * AccZ[i]) * g);
        if (v.back() > maxx)
            maxx = v.back();
        if (v.back() < minn)
            minn = v.back();
        timestamp.push_back(current_time + i * 0.01);
    }

    AccX.clear();
    AccY.clear();
    AccZ.clear();

    /*Compact data in the from of a data class*/
    data df = data(timestamp, v);

    timestamp.clear();
    v.clear();

    /*Detect falls*/
    int falls = fall_detection(df, df.len, 100);

    printf("%d fall(s) detected\n", falls);
    return 0;
}