import sys

import pandas as pd


def covid_trend(county, state, days):
    # Read all us COVID-19 data into a dataframe
    all_us = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
    # Extract out line for specific county and state; Also drop unneeded fields
    all_county_state = all_us[all_us['Province_State'] == state][all_us['Admin2'] == county] \
        .drop(['UID', 'Lat', 'Long_', 'Combined_Key', 'Country_Region', 'Province_State'], axis=1)
    # Do a melt() shift() style operation to capture increase in cases per day
    # use days+1 so that first record in returned value will not have 0 since
    # we use off-stage data from previous day
    all_county_state = all_county_state \
        .melt(id_vars=['Admin2'], var_name='Date', value_name='Cases') \
        .drop('Admin2', 1).tail(days + 1)
    all_county_state['New'] = (all_county_state["Cases"] - all_county_state["Cases"].shift()).fillna(0)
    return (all_county_state.tail(days))


def test_examples():
    print("Shelby County, Tennessee")
    print(covid_trend('Shelby', 'Tennessee', 60))
    print("\nAllegheny, Pennsylvania")
    print(covid_trend('Allegheny', 'Pennsylvania', 10))
    print("\nMonongalia, West Virginia")
    print(covid_trend('Monongalia', 'West Virginia', 10))


n = len(sys.argv)
if (n != 4):
    print("USAGE: python CovidCount.py countyName stateName days")
    sys.exit(1)
county, state, days = sys.argv[1], sys.argv[2], int(sys.argv[3])
covid_report = covid_trend(county, state, days)
print('{0}, {1}\n{2}'.format(county, state, covid_report.to_string(index=False)))
