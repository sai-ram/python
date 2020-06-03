import pandas as pd
import sys

def ny_covid_trend(county,state,days):
	all_us = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
	all_county_state = all_us[all_us['county'] == county][all_us['state'] == state]\
		.drop(['fips','county','state'],axis=1)
	all_county_state['new_cases'] = all_county_state['cases'].diff()
	all_county_state['new_deaths'] = all_county_state['deaths'].diff()
	return (all_county_state.tail(days))

n = len(sys.argv)
if (n != 4):
	print("USAGE: python NyCovidCount.py countyName stateName days")
	sys.exit(1)
county, state, days = sys.argv[1], sys.argv[2], int(sys.argv[3])
covid_report = ny_covid_trend(county, state, days)
print('{0}, {1}\n{2}'.format(county,state,covid_report.to_string(index=False)))
