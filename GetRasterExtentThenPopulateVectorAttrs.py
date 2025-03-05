# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:53:06 2025

@author: GrahamLoewenthal
"""

import os
import glob 
import geopandas as gpd
import rioxarray as rio
from shapely.geometry import box, Polygon


# the list of files to processing
wrk_dir = r"E:\DWER_LIDAR\Working"
glob.glob(os.path.join(wrk_dir, "/*/", "*.tif"), recursive=True)

lst_1st = glob.glob(os.path.join(r"E:\DWER_LIDAR\Working/*/raster/*MGA50_?.tif"), recursive=True)
lst_2nd = glob.glob(os.path.join(r"E:\DWER_LIDAR\Working/*/raster/*MGA50.tif"), recursive=True)
lst_3rd = glob.glob(os.path.join(r"E:\DWER_LIDAR\Working/*/raster/*MGA51.tif"), recursive=True)

# this is a subset
lst_1st = ['E:\\DWER_LIDAR\\Working\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA2020\\raster\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA1994_MGA50_B.tif',
 'E:\\DWER_LIDAR\\Working\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA2020\\raster\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA1994_MGA50_C.tif',
 'E:\\DWER_LIDAR\\Working\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA2020\\raster\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA2020_MGA50_B.tif',
 'E:\\DWER_LIDAR\\Working\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA2020\\raster\\200968_Pilbara_Rivers_Area3_DEM_1m_GDA2020_MGA50_C.tif',]


lst_2nd = ['E:\\DWER_LIDAR\\Working\\200968_Pilbara_Rivers_Area1_DEM_1m_GDA2020\\raster\\200968_Pilbara_Rivers_Area1_DEM_1m_GDA1994_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\200968_Pilbara_Rivers_Area2_DEM_1m_GDA2020\\raster\\200968_Pilbara_Rivers_Area2_DEM_1m_GDA1994_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\Ashburton_LiDAR_1m_DSM_GDA2020\\raster\\Ashburton_LiDAR_1m_DSM_GDA94_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\Burrup_Lidar_30Oct2018_50cm_DSM_Final_GDA2020\\raster\\Burrup_Lidar_30Oct2018_50cm_DSM_Final_GDA94_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\Irwin_River_50cm_DEM_Apr_2023_GDA2020\\raster\\Irwin_River_50cm_DEM_Apr_2023_GDA94_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\Oakajee_LiDAR_Jan_2021_1m_DEM_GDA2020\\raster\\Oakajee_LiDAR_Jan_2021_1m_DEM_GDA94_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\Perth_1m_DEM_GDA2020\\raster\\Perth_1m_DEM_GDA94_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\Shire_of_Denmark_Feb_2023_1m_LiDAR_DEM_GDA2020\\raster\\Shire_of_Denmark_Feb_2023_1m_LiDAR_DEM_GDA1994_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\South_Metro_Jan_2023_1m_DEM_GDA2020\\raster\\South_Metro_Jan_2023_1m_DEM_GDA94_MGA50.tif',
 'E:\\DWER_LIDAR\\Working\\Town_of_Bassendean_1m_DEM_LiDAR_GDA2020\\raster\\Town_of_Bassendean_1m_DEM_LiDAR_GDA94_MGA50.tif']

lst_fin = lst_1st + lst_2nd + lst_3rd
len(lst_fin)


def rasterExtents(rasterFileName, VectorExtentFileName):
    # farie
    print("Reading lazily the raster...")
    xds = rio.open_rasterio(rasterFileName)    

    print("Extracting the bounds of the raster...")
    minx=xds.rio.bounds()[0]
    miny=xds.rio.bounds()[1]
    maxx=xds.rio.bounds()[2]
    maxy=xds.rio.bounds()[3]

    bbox = box(*xds.rio.bounds()) # get bounds from the xds, make a Shapely box    
    polygon = Polygon(bbox) # make the box a make a Shapely polygon

    print("Converting the bounds as a gdf...")
    gdf = gpd.GeoDataFrame(index = [0], crs = xds.rio.crs, geometry = [polygon]) # include the xds defined crs


   
    print("Defining additional columns ...")
    new_col = ["ID",
    "PATH", "FILENAME","FORMAT",
    "ATTRIBUTE",    "DATAUNIT",
    "SOURCE",    "CAPTTYPE",
    "CAPTYEAR",    "FILESIZE", "CRS",
    "SIZE_X", "SIZE_Y", 
    "MAPUNIT", "BANDS", "PIXELTYPE",
    "COLS", "ROWS",    
    "XMIN",    "XMAX",    "YMIN", "YMAX",    
    "METALINK",
    "FILESIZE_B", "FILESIZE_MB", "FILESIZE_GB"]
    
    print("Inserting the columns ...")
    for i in new_col:
        gdf[i]=0
    
    #print(gdf.columns)
    #print(gdf.dtypes)
    
    
    print("Defining column datatypes ...")
    gdf = gdf.astype({
        'ID':'int',
        'PATH':'string',
        'FILENAME':'string',
        "FORMAT": 'string',
        "ATTRIBUTE":'string',
        "DATAUNIT":'string',
        "SOURCE":'string',
        "CAPTTYPE":'string',
        "CAPTYEAR":'int',
        "FILESIZE":'string',
        "CRS":'string',
        "SIZE_X":'int',
        "SIZE_Y":'int',
        "MAPUNIT":'string',
        "BANDS":'int',
        "PIXELTYPE":'string',
        "COLS":'int',
        "ROWS":'int',
        "XMIN":'float32',
        "XMAX":'float32',
        "YMIN":'float32',
        "YMAX":'float32',
        "METALINK":'string',
        "FILESIZE_B":'float32',
        "FILESIZE_MB":'float32',
        "FILESIZE_GB":'float32'
    })
    
    #print(gdf.dtypes)
    
    print("Attributing the records with values...")
    gdf["PATH"] =  str(os.path.split(rasterFileName)[0])
    gdf["FILENAME"] = str(os.path.split(rasterFileName)[1])
    gdf["FORMAT"] = str(os.path.splitext(rasterFileName)[1])
    gdf["ATTRIBUTE"] = "DEM"
    gdf["DATAUNIT"] = "Meters"
    gdf["SOURCE"] = "Landgate"
    gdf["CAPTTYPE"] = "LiDAR"
    gdf["CAPTYEAR"] = "2022-2023"
    gdf["FILESIZE"] = str(round(os.stat(rasterFileName).st_size/(1024*1024),1)) + "MB"
    gdf["CRS"] = str(xds.rio.crs).split(":")[1]
    gdf["SIZE_X"] = int(xds.rio.transform()[0])
    gdf["SIZE_Y"] = int(xds.rio.transform()[0])
    gdf["MAPUNIT"] = "meters"
    gdf["BANDS"] = xds.rio.count # "single" if len(xds.rio.shape) == 2 else "multi"
    gdf["PIXELTYPE"] = "32-bit floating point"
    gdf["COLS"] = xds.rio.width
    gdf["ROWS"] = xds.rio.height
    gdf["XMIN"] = minx
    gdf["XMAX"] = maxx
    gdf["YMIN"] = miny
    gdf["YMAX"] = maxy
    gdf["METALINK"] = "V:\GIS2-Supplement\Data\Imagery\DEM_LIDAR\LIDAR\*\*"
    gdf["FILESIZE_B"] = os.stat(rasterFileName).st_size
    gdf["FILESIZE_MB"] = os.stat(rasterFileName).st_size/(1024*1024)
    gdf["FILESIZE_GB"] = os.stat(rasterFileName).st_size/(1024*1024*1024)


    
    print("Writing the gdf to file...")
    #gdf.to_file(dst_fil + ".geojson', driver='GeoJSON')  
    gdf.to_file(VectorExtentFileName + ".shp")   

    return

for src_fil in lst_fin:
    print(os.path.basename((src_fil.upper())), "\n")
    dst_fil = os.path.splitext(src_fil)[0] + "_extent"
    print("Executing the function")
    rasterExtents(src_fil, dst_fil)
    print(os.path.basename((dst_fil)), "\n")
    


"""
# works
print("Reading lzily the raster...")
xds = rio.open_rasterio(src_fil)    

print("Extracting the bounds of the raster...")
xds.rio.bounds()
bbox = box(*xds.rio.bounds())
polygon = Polygon(bbox)

print("Converting the bounds as a gdf...")
gdf = gpd.GeoDataFrame(index = [0], crs = xds.rio.crs, geometry = [polygon])

print("Writing the gdf to file...")
#gdf.to_file(dst_fil + ".geojson', driver='GeoJSON')  
gdf.to_file(dst_fil + ".shp")   
"""