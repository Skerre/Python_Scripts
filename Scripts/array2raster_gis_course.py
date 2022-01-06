from osgeo import gdal
from osgeo import osr

def array2raster(newRasterfn, dataset, array):

    """
    save GTiff file from numpy.array
    input:
        newRasterfn: save file name
        dataset : original tif file
        array : numpy.array
        dtype: Byte or Float32.
    """
    if len(array.shape) == 3:
        cols = array.shape[2] # 2
        rows = array.shape[1] # 1
    
    if len(array.shape) == 2:
        cols = array.shape[1]
        rows = array.shape[0]
    if dataset:
        originX, pixelWidth, b, originY, d, pixelHeight = dataset.GetGeoTransform()
        
    driver = gdal.GetDriverByName('GTiff')

    # set number of bands.

    if array.ndim == 2:
        band_num = 1
    else:
        band_num = array.shape[0]

    outRaster = driver.Create(newRasterfn, cols, rows, band_num, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    # Loop over all bands.
    for b in range(band_num):
        outband = outRaster.GetRasterBand(b + 1)
        # Read in the band's data into the third dimension of our array
        if band_num == 1:
            outband.WriteArray(array)
        else:
            outband.WriteArray(array[b,:,:])

    # setting srs from input tif file.
    prj=dataset.GetProjection()
    outRasterSRS = osr.SpatialReference(wkt=prj)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()