#ifndef __DEF_FALL_HPP__
#define __DEF_FALL_HPP__

#include <vector>
#include <utility>
#include <iostream>

using std::pair;
using std::vector;

template <typename T>
using data_table = vector<pair<T, T>>;


class data
{
public:
    vector<double> time = {};
    vector<double> v = {};
    int len = 0;

    void add(double t, double v);
    data(vector<double> t, vector<double> v);
};

template <typename T>
data_table<T> delete_items_by_indexes(data_table<T> list, vector<int> indexes);

float max(float a, float b);

float max3(vector<float> li);

double std_dev(vector<float> lst);

double Average(vector<float> lst);

double abs_d(double a);

vector<vector<int>> *find_lists_with_same_number(data_table<float> lst);

int fall_detection(data df2, int step2, int hz);

#endif // __DEF_FALL_HPP__