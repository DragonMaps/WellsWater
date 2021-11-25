import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import folium as fl
import streamlit_folium as sf
import branca.colormap as cm
import os as os
#import wget
import tarfile
import datetime as dt

#st.write('loaded 9 modules')

riverbasins_gdf = gpd.read_file("riverbasins.geojson")
co_counties_gdf = gpd.read_file("co_counties.geojson")

#verify no missing/Nan
riverbasins_gdf.fillna(0.,inplace=True)
riverbasins_gdf.isnull().sum().sum()
co_counties_gdf.fillna(0.,inplace=True)
co_counties_gdf.isnull().sum().sum()

cmax = max(co_counties_gdf['Wells'])
cmin = min(co_counties_gdf['Wells'])

bmax = max(riverbasins_gdf['Wells'])
bmin = min(riverbasins_gdf['Wells'])

st.subheader("Colorado Water Wells by County and River Basin")

#make water map
water_map = fl.Map(location=[co_counties_gdf.centroid.y.mean(),
                              co_counties_gdf.centroid.x.mean()],
                zoom_start=7,tiles=None)
fl.TileLayer('Stamen Toner',name='BackGround',control=False).add_to(water_map)

colormap_counties = cm.linear.Set1_09.scale(0,cmax)

colormap_counties.caption = 'Number of Wells in County'
colormap_counties.add_to(water_map)

colormap_basins = cm.linear.Accent_08.scale(0,bmax)

colormap_basins.caption = 'Number of Wells in Basin'
colormap_basins.add_to(water_map)

# Add county data with mouseover
fl.GeoJson(co_counties_gdf, name='Counties',

           style_function = lambda x: {"weight":0.5, 
                                       'color':'grey',
#                                       'fillColor':'red',
                            'fillColor':colormap_counties(x['properties']['Wells']), 
                            'fillOpacity':0.5
               },
           
               highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.25, 
                                'weight': 0.1
               },
               
               tooltip=fl.GeoJsonTooltip(
                   fields=['LABEL','Wells'],
                   aliases=['County:','Wells:'],
                   labels=True,
                   localize=True
               ),
               ).add_to(water_map)

# Add river data with mouseover
fl.GeoJson(riverbasins_gdf, name='River Basins',
               style_function = lambda x: {"weight":1.0, 
                            'color':'blue',
#                            'fillColor':'transparent', 
                            'fillColor':colormap_basins(x['properties']['Wells']), 
                            'fillOpacity':0.5
               },
           
               highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.25, 
                                'weight': 0.1
               },
               
               tooltip=fl.GeoJsonTooltip(
                   fields=['HU6NAME','Wells'],
                   aliases=['Basin:','Wells:'],
                   labels=True,
                   localize=True
               ),
               ).add_to(water_map)

# Add control
fl.LayerControl(collapsed=False).add_to(water_map)

sf.folium_static(water_map)

st.caption('Source: Colorado Water Convservation Board/Colorado Division of Water Resource')
