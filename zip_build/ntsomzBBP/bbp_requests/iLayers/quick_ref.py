from typing import List
import gdal
import osr
import urllib.request as urlreq

def load_url(url: str, path: str)->bool:
    ret = urlreq.urlretrieve(url, path)
    print(ret)

def georeference(src_filename: str, dst_filename:str, CRS:str, boundingbox:List[float], format:str = "GTiff"):
    # Opens source dataset
    #print(src_filename)
    src_ds = gdal.Open(src_filename)
    driver = gdal.GetDriverByName(format)
    raster_size = [src_ds.RasterXSize, src_ds.RasterYSize]
    # Open destination dataset
    #print(dst_filename)
    dst_ds = driver.CreateCopy(dst_filename, src_ds, 0)
    #print(dst_ds)
    boundingbox = [min(boundingbox[0], boundingbox[2]), min(boundingbox[1], boundingbox[3]), max(boundingbox[0], boundingbox[2]), max(boundingbox[1], boundingbox[3])]
    #print(boundingbox)
    gt = [boundingbox[0], (boundingbox[2]-boundingbox[0])/raster_size[0], 0, boundingbox[3], 0, -(boundingbox[3]-boundingbox[1])/raster_size[1]]
    #print(gt)
    # Get raster projection
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(CRS)
    dest_wkt = srs.ExportToWkt()
    #print(dest_wkt)
    # Set projection
    # Set location
    dst_ds.SetProjection(dest_wkt)
    dst_ds.SetGeoTransform(gt)
    # Close files
    dst_ds = None
    src_ds = None
    

# path_to_png = "D:/Project/NTSOMZ/EKBBP_QGIS_Plugin/ntsomzbbp/preview.png"
# path_to_tiff = 'D:/Project/NTSOMZ/EKBBP_QGIS_Plugin/ntsomzbbp/preview.tiff'
# EPSG = 4326
# bb = [39.552995, 49.404492, 48.192643, 54.477736]
# georeference(path_to_png, path_to_tiff, EPSG, bb)

    
if __name__ == "__main__":
    path_to_png = "D:/Project/NTSOMZ/EKBBP_QGIS_Plugin/ntsomzbbp/preview.png"
    path_to_tiff = 'D:/Project/NTSOMZ/EKBBP_QGIS_Plugin/ntsomzbbp/preview.tiff'
    EPSG = "EPSG:4326"
    "[39,552995, 49,404492, 48,192643, 54,477736]"
    bb = [39.552995, 49.404492, 48.192643, 54.477736]
    print(111)
    georeference(path_to_png, path_to_tiff, EPSG, bb)