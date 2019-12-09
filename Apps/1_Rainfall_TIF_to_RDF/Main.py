from osgeo import gdal
from shapely.geometry import Point
import geopandas as gpd
import csv
import sys

from classes.observation import Observation
from classes.dataset import Dataset


def pixel2coord(ds, x, y):
    # GDAL affine transform parameters, According to gdal documentation
    # xoff/yoff are image left corner, a/e are pixel wight/height and b/d is rotation and is zero if image is north up.
    xoff, a, b, yoff, d, e = ds.GetGeoTransform()
    """Returns global coordinates from pixel x, y coords"""
    xp = a * x + b * y + xoff
    yp = d * x + e * y + yoff
    return xp, yp


def coord2pixel(ds, easting, northing):
    """Transforms lat/lon coordinates to pixel coordinates"""
    tf = ds.GetGeoTransform()
    x = int(round((easting - tf[0]) / tf[1]))
    y = int(round((northing - tf[3]) / tf[5]))
    return x, y


def getSum(gdf, zim, img_array, ds):
    sum = 0
    for index, row in gdf.iterrows():
        if zim.contains(Point(row['geometry'].y, row['geometry'].x)).any():
            # print("Point inside country of interest.")
            latIn = row['geometry'].x
            longIn = row['geometry'].y

            # print("lat: %s long: %s" % (latIn, longIn))

            _x, _y = coord2pixel(ds, longIn, latIn)

            # print("_x: %s _y: %s" % (_x, _y))

            # print(img_array[_y, _x])

            sum += img_array[_y, _x]

            # latsIn.append(latIn)
            # longsIn.append(longIn)
    return sum


def readImage(path):
    # Variables
    longs = []
    lats = []
    vals = []
    rows = 400 + 1
    colms = 500 + 1
    latsIn = []
    longsIn = []
    country = "Malawi"

    ds = gdal.Open(path)

    for row in range(0, rows):
        for col in range(0, colms):
            (x, y) = pixel2coord(ds, col, row)
            lats.append(x)
            longs.append(y)

    for x in lats:
        vals.append("NA")

    geometry = [Point(xy) for xy in zip(longs, lats)]

    crs = {'init': 'epsg:4326'}

    gdf = gpd.GeoDataFrame(vals, crs=crs, geometry=geometry)

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    zim = world[world.name == country]

    rb = ds.GetRasterBand(1)
    img_array = rb.ReadAsArray()  # get the raster as python array

    return ds, img_array, zim, gdf


def getRainfall(path,outputPath):
    short_ns = "eg"

    ds_name = "%s:dataset-%s " % (short_ns, "prices")
    ds_rainfall = Dataset(ds_name)

    # Obtain rainfall aggregate values from CHIRPS
    ds, img_array, zim, gdf = readImage(path)
    total = getSum(gdf, zim, img_array, ds)

    subject1 = "%s:obs1"
    obs1 = Observation(subject=subject1)
    obs1.addDimension(p="dbpedia:month", o="1")
    obs1.addDimension(p="dbpedia:year", o="2015")
    obs1.addMeasure(p="cf-feature:rainfall_amount", o=total)

    print("Total rainfall 2015: %s" % total)

    ds_rainfall.addObservation(obs1)

    ds_rainfall.saveToDisk(outputPath)


if __name__ == "__main__":
    # input = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2015/CHIRPSv2_SouthernAfrica_N30_daystotal_2015-01-01_2015-01-31.tif"
    # outputPath = "/home/mmami/FhG/Projects/BETTER/Data/rdf-rainfall.ttl"

    inpt = sys.argv[1]
    output = sys.argv[2]

    getRainfall(inpt, output)

# chirps14 = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2014/chirps-v2.0.2014.08.tif"
# chirps15 = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2015/CHIRPSv2_SouthernAfrica_N30_daystotal_2015-01-01_2015-01-31.tif"
# chirps16 = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2016/CHIRPSv2_SouthernAfrica_N30_daystotal_2016-01-01_2016-01-31.tif"
# chirps17 = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2017/CHIRPSv2_SouthernAfrica_N30_daystotal_2017-01-01_2017-01-31.tif"
# chirps17_2 = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2017/chirps-v2.0.2017.02.tif"
# chirps18 = "/home/mmami/FhG/Projects/BETTER/Data/CHIRPS/2018/chirps-v2.0.2018.01.tif"

