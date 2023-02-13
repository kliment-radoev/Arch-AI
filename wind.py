from datetime import *
from typing import Any

from meteostat import *
from pandas import *


# ----TEMP----VARIABLES

# total_max_year_list = []
# avg_high_max_year_list = []
# avg_low_max_year_list = []
# avg_medium_year_list = []
# avg_high_min_year_list = []
# avg_low_min_year_list = []
# total_min_year_list = []
# city_coords = []
def wind_parameters(place, period):
    city_coords = ['Sofia, Bulgaria', 42.6977028, 23.3217359]
    lat = city_coords[1]
    lon = city_coords[2]
    city = Point(lat, lon)
    years = period
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
    season_quant_list: list[int | Any] = []
    season_month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                         'October',
                         'November', 'December']

    # -----WIND TEMP AND DIR----VARIABLES

    highest_vals_n_days_in_year = []
    highest_vals_collection = []

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

        # WIND DATA TO LIST

        wspd_list = Series.tolist(data.wspd)
        # print(wspd_list)
        # print(len(wspd_list))
        wpgt_list = Series.tolist(data.wpgt)
        # print(wpgt_list)
        wdir_list = Series.tolist(data.wdir)
        # print(wdir_list)
        wpgt_list = Series.tolist(data.wpgt)
        # print(pdgt_list)
        tavg_list = Series.tolist(data.tavg)
        # print(tavg_list)

        # N DAYS WITH MAX WIND SPEED FOR THE YEAR

        help_list = []
        if i == 1:
            max_wspd_days = []
        mx = 0
        mx_minus_any = 0
        n_windy_days = 5

        mx = max(wspd_list)

        for k in range(n_windy_days):

            if mx in wspd_list:
                ix = wspd_list.index(mx)
                max_wspd_days.append(mx)
                max_wspd_days.append(ix)
                highest_vals_n_days_in_year = []
                highest_vals_n_days_in_year.append('Wind speed: ')
                highest_vals_n_days_in_year.append(mx)
                highest_vals_n_days_in_year.append('Year day: ')
                highest_vals_n_days_in_year.append(ix)
                highest_vals_n_days_in_year.append('Wind dir: ')
                highest_vals_n_days_in_year.append(wdir_list[ix])
                highest_vals_n_days_in_year.append('Temperature: ')
                highest_vals_n_days_in_year.append(tavg_list[ix])
                highest_vals_collection.append(highest_vals_n_days_in_year)

                help_list: list[int | Any] = []

            for j in range(len(wspd_list)):

                mx_minus_any = mx - wspd_list[j]
                if mx_minus_any > 0:
                    help_list.append(mx_minus_any)
                else:
                    pass

            mx_minus_any = min(help_list)
            mx = mx - mx_minus_any
        # print(highest_vals_collection)

        # print(max_wspd_days)

        # ZIP KEYS (WIND SPEED) WITH VALUES (DAY OF YEAR)

        keys_list = []
        vals_list = []
        for keyval in max_wspd_days:
            count += 1
            if count % 2 != 0:
                keys_list.append(keyval)
            elif count % 2 == 0:
                vals_list.append(keyval)

        max_wspd_days_dict = dict(zip(keys_list, vals_list))
        # print(max_wspd_days_dict)
        # print(keys_list)
        # print(vals_list)

        # TEMPERATURE AND DIRECTION FOR THE MAX SPEED DAYS

        # Deep-freeze: < - 15°C;
        # Freeze: - 15°C to 0°C
        # Cold: 0°C to 8.lists°C;
        # Cool: 8.lists°C to 15°C;
        # Room: 15°C to 25°C.
        # Warm: 25°C to 32°C.
        # Hot: 32° to 40°C
        # Excessive heat: > 40°

    temp_ranges = ['Deep-freeze', 'Freeze', 'Cold', 'Cool', 'Optimal', 'Warm', 'Hot', 'Excessive heat']
    temp_range_values = [0, 0, 0, 0, 0, 0, 0, 0]

    for o in range(years * n_windy_days):
        if highest_vals_collection[o][7] <= -15:
            temp_range_values[0] += 1
        elif -15 < highest_vals_collection[o][7] <= 0:
            temp_range_values[1] += 1
        elif 0 < highest_vals_collection[o][7] <= 8:
            temp_range_values[2] += 1
        elif 8 < highest_vals_collection[o][7] <= 15:
            temp_range_values[3] += 1
        elif 15 < highest_vals_collection[o][7] <= 25:
            temp_range_values[4] += 1
        elif 25 < highest_vals_collection[o][7] <= 32:
            temp_range_values[5] += 1
        elif 32 < highest_vals_collection[o][7] <= 40:
            temp_range_values[6] += 1
        elif highest_vals_collection[o][7] > 40:
            temp_range_values[7] += 1

            # DISTRIBUTION OF WINDY DAYS IN MONTHS

    delta_n_years = (end - start) * years
    delta_1_8 = delta_n_years.days / (12 * years)
    # print(delta_1_8)

    for per in range(12):

        if per == 0:
            period_list = [per, per + int(delta_1_8)]
        else:
            period_list.append(int((per * delta_1_8) + delta_1_8))
        # print(period_list)

        for wd in range(len(vals_list)):
            val_check = vals_list[wd]
            if period_list[per] <= val_check < period_list[per + 1]:
                season_val_list[per].append(val_check)

    cnt = 0
    for m in season_val_list:
        mm = len(season_val_list[cnt])
        season_quant_list.append(mm)
        cnt += 1

    broi = 0
    w = 0;
    sp = 0;
    su = 0;
    a = 0
    wdays_per_season_list = []
    for wdd in vals_list:

        if wdd >= 355 or wdd < 80:
            w += 1
        elif 80 <= wdd < 172:
            sp += 1
        elif 172 <= wdd < 265:
            su += 1
        elif 265 <= wdd < 354:
            a += 1
        broi += 1

    season_str_list = ['Winter', 'Spring', 'Summer', 'Autumn']
    wdays_per_season_list = [w, sp, su, a]

    # 1 MONTH AND 1 SEASON

    max_WD_month = max(season_quant_list)
    max_WD_season = max(wdays_per_season_list)
    max_WD_M_index = season_quant_list.index(max_WD_month)
    max_WD_S_index = wdays_per_season_list.index(max_WD_season)
    # print(max_WD_M_index)
    # print(max_WD_S_index)

    month = season_month_list[max_WD_M_index]
    season = season_str_list[max_WD_S_index]

    if city_coords[1] >= 0:
        hemisphere = 'Northern Hemisphere'
    else:
        hemisphere = 'Southern Hemisphere'

    # SECOND AND THIRD WINDY MONTHS

    se_qu_li = season_quant_list[:]
    m_mx = max(se_qu_li)
    windy_months = 5
    h_list = []
    windy_months_list = []

    # print(se_qu_li)

    for z in range(windy_months):
        if m_mx in se_qu_li:
            ii = se_qu_li.index(m_mx)
            windy_months_list.append(m_mx)
            windy_months_list.append(ii)
            se_qu_li[ii] = 0
            h_list: list[int | Any] = []

        for w in range(len(se_qu_li)):

            mx_minus_any = m_mx - se_qu_li[w]
            if mx_minus_any >= 0:
                h_list.append(mx_minus_any)
            else:
                pass

        mx_minus_any = min(h_list)
        m_mx = m_mx - mx_minus_any
        # print(season_quant_list)
        # print(se_qu_li)
        # print(windy_months_list)

    # NAMES OF OTHER WINDY MONTHS

    oth_months_list = []
    oth_speed_list = []

    for md in range(len(windy_months_list)):
        if md == 0 or md == 1:
            continue
        elif md > 2 and md % 2 != 0:
            ind = windy_months_list[md]
            oth_months_list.append(season_month_list[ind])
            oth_speed_list.append(season_quant_list[ind])
        else:
            continue

    # print(oth_months_list)
    oth_months_list_alltoend = oth_months_list[:-1]
    omla = str(oth_months_list_alltoend)
    omla = omla.replace("[", "")
    omla = omla.replace("]", "")
    omla = omla.replace("'", "")
    # print(omla)
    oth_months_list_end = oth_months_list[-1]
    # print(oth_months_list_end)
    month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    month_values = season_quant_list
    month_quant_dict = {month_keys[i]: month_values[i] for i in range(len(month_keys))}

    season_keys = ['Winter', 'Spring', 'Summer', 'Fall']
    season_values = wdays_per_season_list
    season_quant_dict = {season_keys[i]: season_values[i] for i in range(len(season_keys))}

    print(f"WINDS:\n")
    # print(f'Maximum speed {n_windy_days * years} windy days in the last {years} year (day number from the start of the year): \n  {vals_list}\n')
    # print(f'List of year days separating averaged months {chr(8776)} {delta_1_8:.3f} days: \n    {period_list}\n')
    # print(f'List of most windy days distributed by month in the last {years} years starting from January: \n    {season_val_list}\n')
    print(
        f'Number of {n_windy_days * years} high speed windy days for a period of {years} years distributed by month: \n    {month_quant_dict}\n')
    print(
        f'Number of {n_windy_days * years} high speed windy days for a period of {years} years distributed by season: \n    {season_quant_dict}\n')
    print(f'The maximum wind speed for the {years} years period is {max(wspd_list)} km/h\n')
    print(
        f'The most windy season for the {years} years period is the {season} ({hemisphere}) and the most windy month is {month}')
    print(f'Other months with high wind speed are {omla} and {oth_months_list_end}\n')

    print(
        f'In {round(((temp_range_values[0] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[0]}')
    print(
        f'In {round(((temp_range_values[1] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[1]}')
    print(
        f'In {round(((temp_range_values[2] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[2]}')
    print(
        f'In {round(((temp_range_values[3] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[3]}')
    print(
        f'In {round(((temp_range_values[4] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[4]}')
    print(
        f'In {round(((temp_range_values[5] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[5]}')
    print(
        f'In {round(((temp_range_values[6] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[6]}')
    print(
        f'In {round(((temp_range_values[7] / (years * n_windy_days)) * 100), 2)} % of the cases the strongest winds are {temp_ranges[7]}\n')

    # Wind direction in the windiest days?
    # Temperature in the windiest days?
    # Wind peak gust compared to the windiest days and windiest direction?
    # Matrix:
    #               wind speed - wind gust - wind direction - temperature (extremums for all values)
    #    wind speed     23          543             65           234
    #    wind gust      ..          ...             ..           ...
    #    direction      54          ...             11           ...
    #    temperature    ..          ...             ..           ...
