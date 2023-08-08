from osgeo import gdal
import operator
import glob
import numpy as np

def main():
 
    '''Simple tool to crop: Requirements: place a geojson cutline for cropping and tif files in the same folder. 
    Np.nan is being used for NA, resolution defaults to input raster resolution.
    https://gdal.org/api/python/osgeo.gdal.html for gdal warp arguments'''
    tiff_names = glob.glob('*.tif')
    cutline = glob.glob('*.geojson')
    # if we need additional information about the raster
    # print(gdal.Info(tiff_names[0], format='json'))
    names = ["crop_" + sub for sub in tiff_names]
    
    for idx,file in enumerate(tiff_names):

        ds = gdal.Open(file)
        # a quick way to get the xres and yres of the raster file: https://gis.stackexchange.com/questions/368003/how-to-get-raster-resolution-using-gdal
        xres, yres = operator.itemgetter(1,5)(ds.GetGeoTransform())
        # this solution is equivalent and does not require to import operator:
        # transform = ds.GetGeoTransform()
        # pixelWidth = transform[1]
        # pixelHeight = transform[5]

        print("File number {}:".format(idx+1), names[idx])
        gdal.Warp(names[idx], ds, xRes = xres, yRes = yres, resampleAlg = "bilinear",
                  dstSRS = "EPSG:4326", cutlineDSName = cutline[0],
                  cropToCutline = True, dstNodata = np.nan, outputType = gdal.GDT_Float32)
        del ds # https://gis.stackexchange.com/questions/80366/why-close-a-dataset-in-gdal-python
        
if __name__ == "__main__":
    main()
