#############
# This script is for part 3 of my prompt to give some 3d visualization.
# Also has interactivity to meet that requirement of the prompt.
#
# The two 3d surface maps are shown side-by-side due to the scales of both of them being way to far off to show anything meaningful.
#
# Author: Clay Bellou
#############
import sys
import pandas as pd
import numpy as np
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

plotColorScale = "thermal"
if len(sys.argv) == 2:
    plotColorScale = sys.argv[1]
elif len(sys.argv) > 2:
    print("To many color arguments! Using default colors")

#read database files into a table in memory
earthquakes = pd.read_csv("EarthquakeDataWithCountries.csv")
suicides = pd.read_csv("SuicideDataContriesConverted.csv")


#X-axis will just be the years 1995 to 2015. (NOT including 2016)
x_axis = [0] * 21
index = 0
for x in range(1995,2016):
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
#between z2 and z3, only 1 will be used, just leaving both cause it doesn't add much processing time.
#z_axis2 will be total suicides in that country per year
z_axis2 = [[] * len(x_axis)] * len(y_axis)
#z_axis3 will be average suicides per 100k population in that country per year
z_axis3 = [[] * len(x_axis)] * len(y_axis)

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


# Find total suicides in each country per year
total_suicides_per_country_year = dict()
avg_suicides_per_country_year = dict()
for country in targetCountriesList:
    total_suicides_per_country_year[country] = [int(0)] * 2020
    avg_suicides_per_country_year[country] = dict()
    for x in range(0,2020):
        avg_suicides_per_country_year[country][x] = []


index = 0
for rowCountryRaw in suicides['country']:
    if index != 0:
        validCountry = 0
        rowCountry = str(rowCountryRaw)
        for targetCountry in targetCountriesList:
            if rowCountry == targetCountry:
                validCountry = 1
                break
        if validCountry == 1:
            year = int(suicides['year'].iloc[index])
            if year >= 1995:
                total_suicides_per_country_year[rowCountry][year] += int(suicides['suicides_no'].iloc[index])
                avg_suicides_per_country_year[rowCountry][year].append(float(suicides['suicides/100k pop'].iloc[index]))

    index += 1


# Now format total_suicides_per_country_year into z_axis2
index = 0
for countryName in targetCountriesList:
    tempArray = [float(0)] * len(x_axis)
    tempIndex = 0
    for suicideTotalEntry in total_suicides_per_country_year[countryName]:
        suicideTotal = float(suicideTotalEntry)
        if tempIndex >= len(tempArray):
            break
        if suicideTotal != 0:
            tempArray[tempIndex] = suicideTotal
            tempIndex += 1
    z_axis2[index] = tempArray

    index += 1


# Calculate and format avg suicides per 100k data into z_axis3
index = 0
for countryName in targetCountriesList:
    tempArray = [float(0)] * len(x_axis)
    tempIndex = 0
    # print(avg_suicides_per_country_year[countryName].keys())
    for suicideArrayKey in avg_suicides_per_country_year[countryName].keys():
        suicideArray = avg_suicides_per_country_year[countryName][suicideArrayKey]
        if tempIndex >= len(tempArray):
            break
        NumEntries = len(suicideArray)
        if NumEntries != 0:
            total = float(0)
            for suicideNum in suicideArray:
                total += float(suicideNum)
            avgSuicideNum = total / float(NumEntries)
            if avgSuicideNum != 0:
                tempArray[tempIndex] = avgSuicideNum
                tempIndex += 1
    z_axis3[index] = tempArray
    index += 1


######################## Begin making graph ########################

#This commented out code makes the graph have both overlayed on eachother, which sadly makes it look worse.
#fig = go.Figure(data=[
#    go.Surface(z=z_axis1,x=x_axis,y=y_axis,opacity=0.8,name="Max Magnitude of Earthquake",showlegend=True),
#    go.Surface(z=z_axis3,x=x_axis,y=y_axis,opacity=0.8,name="Avg Suicides per 100k Population",showlegend=True),
#])

#This code has the 2 3d graphs be side-by-side instead.
fig = make_subplots(rows=1, cols=2,
                    specs=[[{'is_3d': True}, {'is_3d': True}]],
                    subplot_titles=['Highest Magnitude Earthquake in each country per year', 'Average suicides per 100k population in each country per year'],
                    )
fig.add_trace(go.Surface(z=z_axis1,x=x_axis,y=y_axis,colorbar_x=-0.07,name="Max Magnitude of Earthquake",autocolorscale=False,colorscale=plotColorScale),1,1)
fig.add_trace(go.Surface(z=z_axis3,x=x_axis,y=y_axis,name="Avg Suicides per 100k Population",autocolorscale=False,colorscale=plotColorScale),1,2)
fig.update_layout(title='Earthquake and Suicide 3D Visualization')
fig.update_layout(
    scene=dict(
        xaxis = dict(title='Year'),
        yaxis = dict(title='Country'),
        zaxis = dict(title='Magnitude')
        ),
    scene2=dict(
        xaxis = dict(title='Year'),
        yaxis = dict(title='Country'),
        zaxis = dict(title='Suicides per 100k Population')
        )
)
fig.update_layout(
    font=dict(
        size=13,
        color="RebeccaPurple"
    )
)
fig.show()