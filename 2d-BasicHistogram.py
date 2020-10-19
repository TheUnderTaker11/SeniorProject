#############
# This script is for part 2 of my prompt to give some 2d visualization.
# This is the static histogram version, just showing the average from 1995 to 2015
#
# Author: Clay Bellou
#############

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

color1 = "blue"
color2 = "orange"

# Handle the color-picking accessibility option!
if len(sys.argv) == 2:
    print("To few color arguments! Using default colors")
elif len(sys.argv) == 3:
    print("Using colors ",sys.argv[1], " and ", sys.argv[2], " instead of the default colors!")
    print("(Default colors for this visualization are blue and orange)")
    color1 = sys.argv[1]
    color2 = sys.argv[2]
elif len(sys.argv) > 3:
    print("To many color arguments! Using default colors")

#read database files into a table in memory
earthquakes = pd.read_csv("EarthquakeDataWithCountries.csv")
suicides = pd.read_csv("SuicideDataContriesConverted.csv")

targetCountriesList = ["United States","Russia","Japan","Mexico","Chile","New Zealand","Australia"]

############ Begin Earthquake data calculations ####################################
earthquake_avg_magnitude_country = dict()
earthquake_total_country = dict()
earthquake_2d_array = dict()
graph_earthquake_array = [0.0] * len(targetCountriesList)
graph_total_earthquake_array = [0] * len(targetCountriesList)
for country in targetCountriesList:
    earthquake_2d_array[country] = []
    earthquake_total_country[country] = 0
    earthquake_avg_magnitude_country[country] = float(0.0)

# Fill the 2d array with all magnitude values for earthquakes in each country.
count = 0
for rowCountryRaw in earthquakes['country']:
    if count != 0:
        validCountry = 0
        rowCountry = str(rowCountryRaw)
        for targetCountry in targetCountriesList:
            if rowCountry == targetCountry:
                validCountry = 1
                break
        if validCountry == 1:
            magnitude = float(earthquakes['Magnitude'].iloc[count])
            earthquake_2d_array[rowCountry].append(magnitude)
            earthquake_total_country[rowCountry] += 1

    count += 1


#calculate average for each country using all magnitude values in 2d array
index = 0
for country in targetCountriesList:
    totalNum = len(earthquake_2d_array[country])
    total = float(0.0)
    for magnitudeStr in earthquake_2d_array[country]:
        total += float(magnitudeStr)
    average = total / float(totalNum)
    earthquake_avg_magnitude_country[country] = average
    graph_earthquake_array[index] = average
    graph_total_earthquake_array[index] = earthquake_total_country[country]
    index += 1


########### Begin Suicide data calculations ######################################################
suicides_avg_per_country = dict()
suicide_2d_array = dict()
graph_suicide_array = [0.0] * len(targetCountriesList)

for country in targetCountriesList:
    suicide_2d_array[country] = []
    suicides_avg_per_country[country] = float(0.0)

# Fill the 2d array with all suicides per 100k pop for each country
count = 0
for rowCountryRaw in suicides['country']:
    if count != 0:
        rowCountry = str(rowCountryRaw)
        validCountry = 0
        for targetCountry in targetCountriesList:
            if rowCountry == targetCountry:
                validCountry = 1
                break
        if validCountry == 1:
            suicide_2d_array[rowCountry].append(float(suicides['suicides/100k pop'].iloc[count]))
    count += 1


#calculate average for each country using all suicide float values in 2d array
index = 0
for country in targetCountriesList:
    totalNum = len(suicide_2d_array[country])
    total = float(0.0)
    for suicideStr in suicide_2d_array[country]:
        total += float(suicideStr)
    average = total / float(totalNum)
    suicides_avg_per_country[country] = average
    graph_suicide_array[index] = average
    index += 1

########### Begin plotting/animating the graph #############
fig = plt.figure(figsize=(12,6))
#creating a subplot
ax1 = fig.add_subplot(1,1,1)


ax1.clear()

np.linspace

plot1Color = color1
plot2Color = color2

# Histogram of average magnitude of all earthquakes in each country
# plt.hist(targetCountriesList,weights=graph_earthquake_array, label="total earthquakes", color=plot1Color,bins=2020,alpha=0.5,ec='black',width=0.9,align='right')
# Histogram of total earthquakes in each country
plt.hist(targetCountriesList,weights=graph_total_earthquake_array, label="total earthquakes", color=plot1Color,bins=2020,alpha=0.5,ec='black',width=0.9,align='right')

plt.axis([-1, len(targetCountriesList), 0, 2500])
plt.xlabel('Country',fontsize=14)
ax1.set_xticks(np.arange(len(targetCountriesList)))
ax1.set_xticklabels(targetCountriesList)
plt.ylabel('Total Earthquakes Per Country',color=plot1Color,fontsize=14)
plt.legend(loc='upper left')
plt.title('Overlapping Histogram of Total Earthquakes and Average Suicides per 100k Population 1985 to 2016')

plot2 = plt.twinx()
plot2.hist(targetCountriesList,weights=graph_suicide_array, label="suicides per 100k pop", color=plot2Color,bins=2020,alpha=0.5,ec='black',width=0.9,align='right')
plot2.set_ylabel("Average Suicides per 100k Population",color=plot2Color,fontsize=14)
plot2.set_xticks(np.arange(len(targetCountriesList)))
plot2.set_xticklabels(targetCountriesList)
plt.axis([-1, len(targetCountriesList), 0, 40])
plot2.legend(loc='upper right')

plt.show()