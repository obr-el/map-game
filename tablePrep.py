import csv
import statecapitalgame as scg

fields = ['name', 'population', 'longitude', 'latitude']
stFile = 'st.csv'
sg = scg.StateGame
stateList = []
for name in sg.city_list:
    pop = sg.population[name]
    long = sg.longitude[name]
    lat = sg.latitude[name]
    namelist = [name, pop, long, lat]
    stateList.append(namelist)
with open(stFile, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(stateList)