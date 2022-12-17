# python3
# Subin Jo
# 2022.12.16

import pandas as pd
import folium, io

def getGPS(in_csv):
    """
    <TestCode>
    usecols = ['GPS(0):Lat', 'GPS(0):Long']
    cf = pd.read_csv('SampleData/inspireFLY009.csv', usecols=usecols)
    lines = cf[['GPS(0):Lat', 'GPS(0):Long']].values[:].tolist()"""

    usecols = ['latitude', 'longitude']
    cf = pd.read_csv(in_csv, usecols=usecols)
    lines = cf[['latitude', 'longitude']].values[:].tolist()
    print(lines)
    return lines

def mappingGPS(lines):
    center = lines[0]
    m = folium.Map(location=center, zoom_start=20)
    folium.PolyLine(locations=lines).add_to(m)
    m.add_child(folium.LatLngPopup())
    data = io.BytesIO()
    m.save(data, close_file=False)
    #m.show_in_browser()

    return data

"""
<TestCode>
if __name__ == "__main__":
    lines = getGPS()
    mappingGPS(lines)
"""