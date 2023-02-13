from datetime import *
from math import isnan

from meteostat import *


def temperatures(place, years):
    total_max_year_list = []
    avg_high_max_year_list = []
    avg_low_max_year_list = []
    avg_medium_year_list = []
    avg_high_min_year_list = []
    avg_low_min_year_list = []
    total_min_year_list = []

    city_coords = place
    years = years

    lat = city_coords[1]
    lon = city_coords[2]
    city = Point(lat, lon)
    days_in_dev = 30
    delta_var = 0

    # ----WIND SPEED----VARIABLES

    windspd = []
    period_list = []
    vals_list_all_y = []
    keys_list = []
    vals_list = []
    count = 0
    season_list = ['ssn_1', 'ssn_2', 'ssn_3', 'ssn_4', 'ssn_5', 'ssn_6', 'ssn_7', 'ssn_8', 'ssn_9', 'ssn_10', 'ssn_11',
                   'ssn_12']
    season_val_list = [[], [], [], [], [], [], [], [], [], [], [], []]
    season_month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                         'October',
                         'November', 'December']

    # SET TIME PERIOD

    today = datetime.now()
    first_year = today.year - years
    firstday_of_period = datetime(first_year, 1, 1)
    delta = timedelta(days=(365 * 1))

    for i in range(1, years + 1):

        if i == 1:
            start = firstday_of_period
            end = firstday_of_period + delta
        else:
            start = firstday_of_period + ((i - 1) * delta)
            end = start + delta

        # Get daily data for 2018
        data = Daily(city, start, end)
        data = data.fetch()
        # print(data)
        # Plot line chart including average, minimum and maximum temperature
        # data.plot(y=['tavg', 'tmin', 'tmax'])
        # data.plot(y=['wspd'])
        # plt.show()
        # print(data)

        total_max_year = max(data.tmax)  # 1

        avg_max_year_pre = max(data.tmax)  # 2, 3
        one_row = (data[data.tmax == avg_max_year_pre])
        key_date = one_row.index[0]
        dev = timedelta(days=days_in_dev)
        l_key_date = key_date - dev
        r_key_date = key_date + dev
        small_data = Daily(city, l_key_date, r_key_date)
        small_data = small_data.fetch()
        avg_high_max_year = sum(small_data.tmax) / len(small_data.tmax)
        avg_low_max_year = sum(small_data.tmin) / len(small_data.tmin)

        avg_medium_year = round((sum(data.tavg) / len(data.tavg)), 2)  # 4

        avg_min_year_pre = min(data.tmin)  # 5, 6
        one_row = (data[data.tmin == avg_min_year_pre])
        key_date = one_row.index[0]
        dev = timedelta(days=days_in_dev)
        l_key_date = key_date - dev
        r_key_date = key_date + dev
        small_data = Daily(city, l_key_date, r_key_date)
        small_data = small_data.fetch()
        avg_high_min_year = sum(small_data.tmax) / len(small_data.tmax)
        avg_low_min_year = sum(small_data.tmin) / len(small_data.tmin)

        total_min_year = min(data.tmin)  # 7

        total_max_year_list.append(total_max_year)  # 1
        total_max_year_list = [x for x in total_max_year_list if isnan(x) == False]
        avg_high_max_year_list.append(avg_high_max_year)  # 2
        avg_high_max_year_list = [x for x in avg_high_max_year_list if isnan(x) == False]
        avg_low_max_year_list.append(avg_low_max_year)  # 3
        avg_low_max_year_list = [x for x in avg_low_max_year_list if isnan(x) == False]
        avg_medium_year_list.append(avg_medium_year)  # 4
        avg_medium_year_list = [x for x in avg_medium_year_list if isnan(x) == False]
        avg_high_min_year_list.append(avg_high_min_year)  # 5
        avg_high_min_year_list = [x for x in avg_high_min_year_list if isnan(x) == False]  # 6
        avg_low_min_year_list.append(avg_low_min_year)
        avg_low_min_year_list = [x for x in avg_low_min_year_list if isnan(x) == False]  # 7
        total_min_year_list.append(total_min_year)
        total_min_year_list = [x for x in total_min_year_list if isnan(x) == False]

    total_max_n_years = round(sum(total_max_year_list) / len(total_max_year_list), 2)
    avg_high_max_n_years = round(sum(avg_high_max_year_list) / len(avg_high_max_year_list), 2)
    avg_low_max_n_years = round(sum(avg_low_max_year_list) / len(avg_low_max_year_list), 2)
    avg_medium_n_years = round(sum(avg_medium_year_list) / len(avg_medium_year_list), 2)
    avg_high_min_n_years = round(sum(avg_high_min_year_list) / len(avg_high_min_year_list), 2)
    avg_low_min_n_years = round(sum(avg_low_min_year_list) / len(avg_low_min_year_list), 2)
    total_min_n_years = round(sum(total_min_year_list) / len(total_min_year_list), 2)

    print(f"TEMPERATURES:\n")
    print(f"Total MAX Summer Temperature averaged for {years} years: {total_max_n_years}")
    print(f"High Summer Temperatures averaged for {years} years: {avg_high_max_n_years}")
    print(f"Low Summer Temperatures averaged for {years} years: {avg_low_max_n_years}")
    print(f"Medium Mild Temperatures averaged for {years} years: {avg_medium_n_years}")
    print(f"High Winter Temperatures averaged for {years} years: {avg_high_min_n_years}")
    print(f"Low Winter Temperatures averaged for {years} years: {avg_low_min_n_years}")
    print(f"Total MIN Winter Temperatures averaged for {years} years: {total_min_n_years}\n")

    temp_list_keys = ["total_max_n_years", "avg_high_max_n_years", "avg_low_max_n_years", "avg_medium_n_years",
                      "avg_high_min_n_years", "avg_low_min_n_years", "total_min_n_years"]
    temp_list_values = [total_max_n_years, avg_high_max_n_years, avg_low_max_n_years, avg_medium_n_years,
                        avg_high_min_n_years, avg_low_min_n_years, total_min_n_years]
    temp_list = dict(zip(temp_list_keys, temp_list_values))

    with open('var_file.txt', 'w') as f:
        f.write('weather_data = ' + str(temp_list) + '\n')
