import pandas as pd
import sys
import datetime
from datetime import timedelta
from datetime import datetime


drop_fields = ['iso_code','continent','date','new_cases_smoothed','new_deaths_smoothed',
'new_cases_per_million','new_cases_smoothed_per_million','new_deaths_per_million',
'new_deaths_smoothed_per_million','reproduction_rate','icu_patients',
'icu_patients_per_million','hosp_patients','hosp_patients_per_million',
'weekly_icu_admissions','weekly_icu_admissions_per_million','weekly_hosp_admissions',
'weekly_hosp_admissions_per_million','new_tests','total_tests',
'new_tests_per_thousand','new_tests_smoothed','new_tests_smoothed_per_thousand',
'tests_units','stringency_index','population','population_density','median_age',
'aged_65_older','aged_70_older','gdp_per_capita','extreme_poverty',
'cardiovasc_death_rate','diabetes_prevalence','female_smokers','male_smokers',
'handwashing_facilities','hospital_beds_per_thousand','life_expectancy',
'human_development_index','new_cases','new_deaths','total_cases','total_deaths']

cols_to_use = ['location','total_cases_per_million','total_deaths_per_million', 
'total_tests_per_thousand','positive_rate','date','tests_per_case']

# def owind_trend():
# 	all_data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv',
# 			index_col='location', usecols=cols_to_use)
# 	current_time = datetime.now() - timedelta(days = 1) 
# 	yesterday = "{}-{}-{}".format(current_time.year, current_time.month, current_time.day)
# 	this_friday_predicate = (all_data['date'] == yesterday)
# 	this_friday_data = all_data[this_friday_predicate].drop(['date'],axis=1)
# 	return(this_friday_data)

def owind_trend():
	all_data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
	current_time = datetime.now() - timedelta(days = 1) 
	yesterday = "{}-{}-{}".format(current_time.year, current_time.month, current_time.day)
	this_friday_predicate = (all_data['date'] == yesterday)
	this_friday_data = all_data[this_friday_predicate].drop(drop_fields,axis=1)
	return(this_friday_data)

n = len(sys.argv)
if ( n == 2):
	sort_field = sys.argv[1]
else:
	sort_field = 'tests_per_case'
owind_tr = owind_trend().rename(columns={'location': 'Country','total_cases_per_million': 'cases_per_million',
	'total_deaths_per_million': 'deaths_per_million', 'total_tests_per_thousand': 'tests_per_thousand'})
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
print(owind_tr.fillna(0.0).sort_values(by=sort_field, ascending=False).to_string(index=False,justify='left'))

