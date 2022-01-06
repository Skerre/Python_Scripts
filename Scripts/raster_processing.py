import osgeo_utils.gdal_merge as gm
from osgeo import gdal
import os
import glob
import subprocess
import rasterio
import geopandas as gpd
import pandas as pd

def merge(path, seperate = True):
    '''Attributes:
    path: set the path where the tif files are located
    seperate: default = True, if false: raster will not be merged per layer but as mosaic
    Output Filename is 'merged.tif' '''

    os.chdir(path)
    files = glob.glob(path+"*tif")
    if seperate == True:
        gm.main(['','-co', 'COMPRESS=LZW', '-separate', '-o', 'merged.tif'] + files)
    else:
        gm.main(['','-co','COMPRESS=LZW', '-o', 'merged.tif'] + files)
def rescale(path, scalefactor = 1):
    '''
    Use this function for a folder you placed the to be rescaled images
    Attributes:
    path: set the path where the tif files are located
    scalefactor = def 1; determines how much the new pixel size will change: 0.5 means that the size will half; 2 means it will double.

    '''
    os.chdir(path)
    files = glob.glob(path+"*tif")
    dims = ()
    for file in files:
        src = gdal.Open(file)
        dims.append(src.RasterXSize, src.RasterYSize)
        src = None


    dataset = gdal.Open(files[0], gdal.GA_ReadOnly)
    dataset = None
    xdim = dataset.RasterXSize * scalefactor
    ydim = dataset.RasterYSize *scalefactor
    for i in range(len(files)):
        result = subprocess.call("gdal_translate -of GTiff -outsize %s %s -r bilinear %s %s" % (xdim, ydim, files[i], files[i]+"_res"))
        print("Success", "x %s y %s oldname %s newname %s" % (xdim, ydim, files[i], files[i]+"_res"))

def clip_all(path, AOI):
    '''
    Use this function for clipping all images with an rectangular AOI
    Attributes:
    path: set the path where the tif files are located
    AOI = format : <ulx> <uly> <lrx> <lry>
    '''
    os.chdir(path)
    if path == None:
        path = ""
    if AOI == None:
        ds = gdal.Open(path)
        ulx, xres, xskew, uly, yskew, yres  = ds.GetGeoTransform()
        lrx = ulx + (ds.RasterXSize * xres)
        lry = uly + (ds.RasterYSize * yres)
        AOI = [ulx,uly,lrx,lry]

    for file in glob.glob("*.tif"):
        ds = gdal.Open(path+file)
        ds = gdal.Translate(path + 'clp' + file, ds, projWin = AOI)
        print("Done: ", path + 'clp' + file)
        ds = None

def pointsampling(path):

    '''
    This tool has been tested on the 26th of December 2021
    This function is used for point sampling.
    Input is a shapefile with point geometries.
    The folder needs to contain the raster files which need to be sampled and the corresponding point shapefiles.
    Returns: points (geopandas)
    '''
    os.chdir(path)
    shp = glob.glob(path + "*.shp")
    try:
        pts = gpd.read_file(shp[0])
        pts.index = range(len(pts))
        coords = [(x,y) for x, y in zip(pts['geometry'].x, pts['geometry'].y)]
        filenames = [file for file in glob.glob("*.tif")]

        for i in range(len(filenames)):
            src = rasterio.open(glob.glob(path + "*.tif")[i])
            pts['{} {}'.format(filenames[i], i + 1)] = [x for x in src.sample(coords, indexes = 1)]
        return(pts)
    except:
        print("No Shapefile")
