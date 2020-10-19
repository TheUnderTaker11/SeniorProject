import sys
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from plotly.subplots import make_subplots

#read database files into a table in memory
earthquakes = pd.read_csv("EarthquakeDataWithCountries.csv")
suicides = pd.read_csv("SuicideDataContriesConverted.csv")




#X-axis will just be the years 1995 to 2016. (NOT including 2017)
x_axis = [0] * 22
index = 0
for x in range(1995,2017):
    x_axis[index] = x
    index += 1

#Y-Axis will be the countries
targetCountriesList = ["United States","Russia","Japan","Mexico","Chile","New Zealand","Australia"]
y_axis = targetCountriesList

#Z-axis MUST BE AN ARRAY OF ARRAYS
#Total number of arrays ( len(z_axis) ) indicates the total Y values aka all countries
#Total entries within each inner array ( len(z_axis[0]) ) indicates the total X values.
#z_axis1 will be the highest magnitude earthquake in that country per year.
z_axis1 = [[] * len(x_axis)] * len(y_axis)
#z_axis2 will be total suicides in that country per year
z_axis2 = [[] * len(x_axis)] * len(y_axis)


#Find the highest magnitude earthquake in each year, which will then be used below to populate z_axis1
highest_magnitude_per_country_year = dict()
for country in targetCountriesList:
    highest_magnitude_per_country_year[country] = [float(0)] * 2020
index = 0
for rowCountryRaw in earthquakes['country']:
    if index != 0:
        validCountry = 0
        rowCountry = str(rowCountryRaw)
        for targetCountry in targetCountriesList:
            if rowCountry == targetCountry:
                validCountry = 1
                break
        if validCountry == 1:
            dateArray = str(earthquakes['Date'].iloc[index]).split("/")
            if len(dateArray) == 3:
                year = int(dateArray[2])
                # Only respect values from 1995 or above
                if year >= 1995:
                    magnitude = float(earthquakes['Magnitude'].iloc[index])
                    if highest_magnitude_per_country_year[rowCountry][year] < magnitude:
                        highest_magnitude_per_country_year[rowCountry][year] = magnitude

    index += 1

#populate z_axis1 with the earthquake data, index 0 of inner array corresponds to 1995, then goes to 2015
index = 0
for countryName in targetCountriesList:
    tempArray = [float(0)] * len(x_axis)
    tempIndex = 0
    for magnitudeEntry in highest_magnitude_per_country_year[countryName]:
        magnitude = float(magnitudeEntry)
        if tempIndex >= len(tempArray):
            break
        if magnitude != 0:
            tempArray[tempIndex] = magnitude
            tempIndex += 1
    z_axis1[index] = tempArray

    index += 1




######################## Begin making graph ########################
fig = go.Figure(data=[go.Surface(z=z_axis1, x=x_axis, y=y_axis)])
fig.update_layout(title='Test graph')
fig.show()