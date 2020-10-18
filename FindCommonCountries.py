#############
# This script was created so I could find a list of candidates to use for a Country-based visualization
#
# Author: Clay Bellou
#############
import pandas as pd
import numpy as np

earthquakes = pd.read_csv("EarthquakeDataWithCountries.csv")
suicides = pd.read_csv("SuicideDataContriesConverted.csv")

################ Earthquake data section
eq_country_dict = dict()
for country in earthquakes['country']:
    hasKey = 0
    for key in eq_country_dict.keys():
        if(key == country):
            hasKey = 1
            break
    if(hasKey == 1):
        eq_country_dict[country] = eq_country_dict[country] + 1
    else:
        eq_country_dict[country] = 1

# print(eq_country_dict)

for dummyVar in range(0,len(eq_country_dict.keys())):
    topCountryValue = 0
    topCountry = "None"
    for key in eq_country_dict.keys():
        if(eq_country_dict[key] > topCountryValue):
            topCountryValue = eq_country_dict[key]
            topCountry = key
    if topCountry != "None" and topCountryValue > 100:
        eq_country_dict[topCountry] = -1
        print(topCountry, " with this many entries: ", topCountryValue)




################ Suicide data section
print("STARTING SUICIDE PART -----------------------------------------------------------------------------------------------------------")
suicide_country_dict = dict()
for country in suicides['country']:
    hasKey = 0
    for key in suicide_country_dict.keys():
        if(key == country):
            hasKey = 1
            break
    if(hasKey == 1):
        suicide_country_dict[country] = suicide_country_dict[country] + 1
    else:
        suicide_country_dict[country] = 1

# print(eq_country_dict)

for dummyVar in range(0,len(suicide_country_dict.keys())):
    topCountryValue = 0
    topCountry = "None"
    for key in suicide_country_dict.keys():
        if(suicide_country_dict[key] > topCountryValue):
            topCountryValue = suicide_country_dict[key]
            topCountry = key
    if topCountry != "None" and topCountryValue > 100:
        suicide_country_dict[topCountry] = -1
        print(topCountry, " with this many entries: ", topCountryValue)