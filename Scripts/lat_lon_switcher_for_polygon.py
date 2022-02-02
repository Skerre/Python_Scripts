### get lat lon from polygon

import geopandas as gpd
import copy

def main():

    shp = gpd.read_file(r"C:\Users\martin.szigeti\Documents\UN Work\social vulnerability index\Notebooks\Data\Albania\Shapefiles/simplified.shp")
    shp = shp.explode()
    points = []
    for polygon in shp.geometry:
        points.extend(polygon.exterior.coords[:-1])
    list_of_lists = [list(elem) for elem in points]
    copyl = copy.deepcopy(list_of_lists)
    for i in range(len(list_of_lists)):
        copyl[i][0] = list_of_lists[i][1]
        copyl[i][1] = list_of_lists[i][0]
    return copyl
if __name__ == '__main__':
    main()