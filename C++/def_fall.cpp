#include "def_fall.hpp"
#include <cmath>
#include <map>
#include <algorithm>
#include <stdexcept>
#include <numeric>

using std::map;

const float g = 9.807;

data::data(vector<double> t, vector<double> v)
{
    try
    {
        if (t.size() != v.size())
            throw std::invalid_argument("Error: t and v must be the same size");
        else
        {
            this->len = t.size();
            this->time = t;
            this->v = v;
        }
    }
    catch (const std::invalid_argument &e)
    {
        std::cerr << e.what() << '\n';
    }
}

void data::add(double t, double v)
{
    this->time.push_back(t);
    this->v.push_back(v);
    this->len++;
}

/*Delete the indexes of the list1 which are given to list2*/
template <typename T>
data_table<T> delete_items_by_indexes(data_table<T> list, vector<int> indexes)
{
    data_table<T> new_list = {};
    for (int i = 0; i < list.size(); i++)
        if (find(indexes.begin(), indexes.end(), i) == indexes.end())
            new_list.push_back(list[i]);
    return new_list;
}

double abs_d(double a)
{
    if (a < 0)
        return -a;
    else
        return a;
}

float max(float a, float b)
{
    if (a > b)
        return a;
    else
        return b;
}

double max3(vector<double> li)
{
    if (li.size() == 0)
        return 0;
    else
        return *max_element(li.begin(), li.end());
}

double std_dev(vector<double> lst)
{
    float avg = accumulate(lst.begin(), lst.end(), 0.0) / lst.size();
    float sq_sum = 0.0;
    for (auto &i : lst)
        sq_sum += (i - avg) * (i - avg);
    return sqrt(sq_sum / (lst.size() - 1));
}

/*A list of lists is sent to the find_lists_with_same_number function that calculates if there are double connections*/
vector<vector<int>> *find_lists_with_same_number(data_table<double> lst)
{
    map<double, vector<int>> number_indexes_0;
    map<double, vector<int>> number_indexes_1;

    for (int i = 0; i < lst.size(); i++)
    {
        double number_0 = lst[i].first;
        double number_1 = lst[i].second;

        if (number_indexes_0.find(number_0) == number_indexes_0.end())
            number_indexes_0[number_0] = {i};
        else
            number_indexes_0[number_0].push_back(i);

        if (number_indexes_1.find(number_1) == number_indexes_1.end())
            number_indexes_1[number_1] = {i};
        else
            number_indexes_1[number_1].push_back(i);
    }

    vector<vector<int>> result_0 = {};
    vector<vector<int>> result_1 = {};

    for (auto const &[key, val] : number_indexes_0)
        if (val.size() > 1)
            result_0.push_back(val);

    for (auto const &[key, val] : number_indexes_1)
        if (val.size() > 1)
            result_1.push_back(val);

    vector<vector<int>> *result = new vector<vector<int>>[2];
    result[0] = result_0;
    result[1] = result_1;

    return result;
}

double Average(vector<double> lst)
{
    return accumulate(lst.begin(), lst.end(), 0.0) / lst.size();
}

/*  The fall_detections function applies the fall detection tast and takes as arguments
    a data class that contains in vector v the magnitudes, and in vector time
    the corresponding timestamps, the length of the time-series and the
    frequency of the sensor that is used.*/
int fall_detection(data df2, int step2, int hz)
{

    vector<double> time = {};
    vector<double> v = {};

    for (int i = 0; i < df2.len; i++)
    {
        time.push_back(df2.time[i]);
        v.push_back(df2.v[i]);
    }

    /*  Create the entries  */
    vector<double> entries = {0};

    for (int i = 1; i < df2.len; i++){
        entries.push_back(((double)(time[i] - time[i-1]) / 10) + entries[i - 1] + 100 / hz);

    }

    data df = data(entries, v);

    /* Calculate the average of the acceleration magnitudes */
    double v_avg = Average(v);

    data_table<double> fall = {};
    data_table<double> new_fall = {};
    data_table<int> index = {};
    data_table<int> new_index = {};

    vector<int> low = {};
    vector<int> high = {};

    float min_limit = 6.5;
    double max_limit = max(v_avg, 20) + 10;
    float max_limi2 = max_limit;

    int fall_duration = 105;
    int fall_limitation = 85;

    int sub_1 = 50;
    int dist_1 = 100;
    int dist_2 = 100;

    /*Find lows and highs */
    for (int i = 0; i < df.len; i++)
    {
        if (df.v[i] < min_limit)
            low.push_back(i);
        else if (df.v[i] > max_limit)
            high.push_back(i);
    }

    if (low.size() != 0 && high.size() != 0)
    {
        vector<int> new_low = {};
        vector<int> new_high = {};

        new_low.push_back(low[0]);
        new_high.push_back(high[0]);

        /* Create the sets of lows */
        for (int i = 1; i < low.size(); i++)
        {
            if (df.time[low[i]] - df.time[low[i - 1]] > sub_1)
            {
                new_low.push_back(low[i - 1]);
                new_low.push_back(low[i]);
            }
            else if (i == low.size() - 1)
                new_low.push_back(low[i]);
        }

        if (new_low.size() % 2 != 0)
            new_low.push_back(new_low[new_low.size() - 1]);

        /* Create the sets of highs */
        for (int i = 1; i < high.size(); i++)
        {
            if (df.time[high[i]] - df.time[high[i - 1]] > sub_1)
            {
                new_high.push_back(high[i - 1]);
                new_high.push_back(high[i]);
            }
            else if (i == high.size() - 1)
                new_high.push_back(high[i]);
        }
        if (new_high.size() % 2 != 0)
            new_high.push_back(new_high[new_high.size() - 1]);

        /*Make the connection of lows and highs which correspond to possible falls*/
        for (int i = 0; i < new_low.size(); i += 2)
            for (int j = 0; j < new_high.size(); j += 2)
            {
                if ((df.time[new_high[j + 1]] - df.time[new_low[i]] < fall_duration) && (df.time[new_high[j + 1]] - df.time[new_low[i]] > 0))
                {
                    fall.push_back({df.time[new_low[i]], df.time[new_high[j + 1]]});
                    index.push_back({new_low[i], new_high[j + 1]});
                }
                else if ((df.time[new_high[j + 1]] - df.time[new_low[i + 1]] < fall_duration) && (df.time[new_high[j + 1]] - df.time[new_low[i + 1]] > 0))
                {
                    fall.push_back({df.time[new_low[i + 1]], df.time[new_high[j + 1]]});
                    index.push_back({new_low[i + 1], new_high[j + 1]});
                }
                else if ((df.time[new_high[j]] - df.time[new_low[i]] < fall_duration) && (df.time[new_high[j]] - df.time[new_low[i]] > 0))
                {
                    fall.push_back({df.time[new_low[i]], df.time[new_high[j]]});
                    index.push_back({new_low[i], new_high[j]});
                }
                else if ((df.time[new_high[j]] - df.time[new_low[i + 1]] < fall_duration) && (df.time[new_high[j]] - df.time[new_low[i + 1]] > 0))
                {
                    fall.push_back({df.time[new_low[i + 1]], df.time[new_high[j]]});
                    index.push_back({new_low[i + 1], new_high[j]});
                }
            }

        new_index = index;
        new_fall = fall;
        vector<int> indexes_to_del = {};

        if (new_fall.size() != 0)
        {
            vector<vector<int>> *same_num_indexes = find_lists_with_same_number(new_fall);

            /*Find the double connections of lows*/
            if (same_num_indexes[0].size() != 0)
                for (int i = 0; i < same_num_indexes[0].size(); i++)
                    for (int j = 1; j < same_num_indexes[0][i].size(); j++)
                    {
                        double sub1 = abs_d(fall[same_num_indexes[0][i][j - 1]].first - fall[same_num_indexes[0][i][j - 1]].second);
                        double sub2 = abs_d(fall[same_num_indexes[0][i][j]].first - fall[same_num_indexes[0][i][j]].second);

                        if (sub1 < sub2)
                            indexes_to_del.push_back(same_num_indexes[0][i][j]);
                        else
                            indexes_to_del.push_back(same_num_indexes[0][i][j - 1]);
                    }
            /*Find the double connections of highs*/
            if (same_num_indexes[1].size() != 0)
                for (int i = 0; i < same_num_indexes[1].size(); i++)
                    for (int j = 1; j < same_num_indexes[1][i].size(); j++)
                    {
                        double sub1 = abs_d(fall[same_num_indexes[1][i][j - 1]].first - fall[same_num_indexes[1][i][j - 1]].second);
                        double sub2 = abs_d(fall[same_num_indexes[1][i][j]].first - fall[same_num_indexes[1][i][j]].second);

                        if (sub1 < sub2)
                            indexes_to_del.push_back(same_num_indexes[1][i][j]);
                        else
                            indexes_to_del.push_back(same_num_indexes[1][i][j - 1]);
                    }

           // delete same_num_indexes;
           same_num_indexes = NULL;
        }
        /*Delete the longer double connection and keep the shorter*/
        if (indexes_to_del.size() != 0)
        {
            new_index = delete_items_by_indexes(new_index, indexes_to_del);
            new_fall = delete_items_by_indexes(new_fall, indexes_to_del);
        }

        /*If the fall is long, search if there are more lows close to the high and trasport the start of the fall to a closer low (Check 1)*/
        int indexx = 0;
        for (int i = 0; i < new_fall.size(); i++)
            if (abs_d(new_fall[i].second - new_fall[i].first) > fall_limitation)
            {
                for (int j = new_index[i].first; j < new_index[i].second; j++)
                    if (df.v[j] < min_limit && (new_index[i].second - j) > 5)
                        indexx = j;

                if (indexx != new_index[i].first)
                {
                    new_index[i].first = indexx;
                    new_fall[i].first = entries[indexx];
                }
            }

        data_table<int> temp_index = {};
        data_table<double> temp_fall = {};

        /*Reject the fall if it is long (Check 2)*/
        for (int i = 0; i < new_fall.size(); i++)
        {
            if (abs_d(abs_d(new_fall[i].first) - abs_d(new_fall[i].second)) < fall_limitation)
            {
                temp_index.push_back(new_index[i]);
                temp_fall.push_back(new_fall[i]);
            }
        }

        new_index = temp_index;
        new_fall = temp_fall;

        temp_fall.clear();
        temp_index.clear();

        vector<double> v_after_fall = {};
        /*Keep the fall if the peak is the highest magnitude or the magnitudes after the fall are close to g (Check 3)*/
        for (int i = 0; i < new_index.size(); i++)
        {
            double max_v = 0;

            for (int j = new_index[i].first - 1; j < new_index[i].second + 1; j++)
                if (df.v[j] > max_v)
                    max_v = df.v[j];

            double t1 = new_fall[i].first - 1 - dist_1;
            double t2 = new_fall[i].second + 1 + dist_2;

            double j1 = 0, j2 = df.v.size() - 1;

            for (int j = new_index[i].first - 1; j > 0; j--)
            {
                if (new_fall[i].first < t1)
                {
                    j1 = j;
                    break;
                }
                else
                    j1 = j;
            }

            for (int j = new_index[i].second + 1; j < df.v.size(); j++)
            {
                if (new_fall[i].second > t2)
                {
                    j2 = j;
                    break;
                }
                else
                    j2 = j;
            }

            vector<double> high1 = {};
            vector<double> high2 = {};

            for (int j = j1; j < new_index[i].first - 1; j++)
                if (df.v[j] > max_limit)
                    high1.push_back(df.v[j]);

            for (int j = new_index[i].second + 1; j < j2; j++)
            {
                if (df.v[j] > max_limit)
                    high2.push_back(df.v[j]);
                if (abs_d(entries[j] - new_fall[i].second) > 0.3)
                    v_after_fall.push_back(df.v[j]);
            }

            double v_avg_after_fall = Average(v_after_fall);

            if ((v_avg_after_fall < g + 2 && v_avg_after_fall > g - 2 && std_dev(v_after_fall) < 2 && v_after_fall.size() > 30) || max_v > max(max3(high1), max3(high2)))
            {
                temp_index.push_back(new_index[i]);
                temp_fall.push_back(new_fall[i]);
            }

            v_after_fall.clear();
            high1.clear();
            high2.clear();
        }

        new_index = temp_index;
        new_fall = temp_fall;

        temp_fall.clear();
        temp_index.clear();
    }

    return new_fall.size();
}
