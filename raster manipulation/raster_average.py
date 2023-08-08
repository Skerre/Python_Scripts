from osgeo import gdal
import glob
import os

def main():

    '''
    Reads every raster layer in a directory and averages them. 
    Inspired by: https://gis.stackexchange.com/questions/376144/how-to-average-multiple-geotiff-images'''
    
    tiff_names = glob.glob('*.tif')

    val = []
    for _,file in enumerate(tiff_names):
        # dirpath = os.path.dirname(__file__)
        # print(os.path.basename)
        print(os.path.abspath(file))
        # print(type(file))
        
        ds = gdal.Open(os.path.abspath(file))
        col   = ds.RasterXSize
        rows  = ds.RasterYSize
        driver = ds.GetDriver()
        val.append(ds.GetRasterBand(1).ReadAsArray().flatten())

    # calculate the average-data
    print(type(val))
    print(len(val))
    
    avg = sum(val)/len(tiff_names)
    len(avg)
    avgdataMatrix= avg.reshape(rows,col)

    raster_avg = driver.Create("avg_" + ".tif", col, rows, 1, gdal.GDT_Float32)
    # here you copy the properties from another raster.
    raster_avg.SetGeoTransform(ds.GetGeoTransform())
    raster_avg.SetProjection(ds.GetProjection())

    # finally, you add the avg data to your new raster

    raster_avg.GetRasterBand(1).WriteArray(avgdataMatrix)
    # raster_avg.GetRasterBand(1).SetNoDataValue(NaN)

    raster_avg = None
    del raster_avg
    del val
    del ds

if __name__ == "__main__":
    main()