import pandas as pd
import sys


drop_fields = ['iso_code','date','continent','new_cases_smoothed','new_deaths_smoothed',
'total_cases_per_million','new_cases_per_million','new_cases_smoothed_per_million',
'new_deaths_smoothed_per_million','icu_patients','icu_patients_per_million',
'hosp_patients','hosp_patients_per_million','weekly_icu_admissions',
'weekly_icu_admissions_per_million','weekly_hosp_admissions',
'weekly_hosp_admissions_per_million','new_tests','new_tests_per_thousand',
'new_tests_smoothed','new_tests_smoothed_per_thousand','tests_per_case','tests_units',
'stringency_index','population','population_density','aged_65_older', 'aged_70_older',
'human_development_index','extreme_poverty','total_cases','new_cases','total_deaths',
'new_deaths','total_deaths_per_million','new_deaths_per_million',
'reproduction_rate', 'total_tests', 'total_tests_per_thousand', 'positive_rate',
'female_smokers','male_smokers','handwashing_facilities','hospital_beds_per_thousand']

def owind_trend():
	all_data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
	this_friday_predicate = (all_data['date'] == '2020-11-13')
	this_friday_data = all_data[this_friday_predicate].drop(drop_fields,axis=1)
	return(this_friday_data)

n = len(sys.argv)
if ( n == 2):
	sort_field = sys.argv[1]
else:
	sort_field = 'life_expectancy'
owind_tr = owind_trend()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
print(owind_tr.fillna(0.0).sort_values(by=sort_field, ascending=False).to_string(index=False))

