from qgis.core import *
from qgis.PyQt.QtWidgets import QListWidgetItem, QTableWidgetItem, QMessageBox
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from typing import List, Union
from ..bbp_objects import TileService, Scene, Product
from ..bbp_key import APIKey
from .quick_ref import georeference, load_url
from os.path import dirname

class TypeEnum:
    """
    Static Enumeration
    """
    File:str = "file"
    WebService:str = "wms"
    XYZService:str = "xyz"
    Preview:str = "preview"


class LayerInfo:
    URL:str = ""
    Type:str = ""
    name:str = ""
    def __init__(self, URL:str, Type:str, name:str):
        self.URL = URL
        self.Type = Type
        self.name = name
    
    def __str__(self):
        ret = "Name: "+self.name+", Path: "+ self.URL+", Type: "+self.Type
        return ret

def create_raster_XYZ(url:str, name:str, additional_str:str = None, projection: str = "EPSG3857", boundingRect: QgsRectangle = None, zmin:int = 0, zmax:int = 18):
    dataSource:str = "url="+url#+additional_str
    typestr:str = "type=xyz"
    zmax:str = "zmax="+str(zmax)
    zmin:str = "zmin="+str(zmin)
    crs:str = "crs="+projection.replace(":","")
    dataSource = "&".join([typestr, dataSource, zmax,zmin,crs])
    rasterLayer = None
    try:
        rasterLayer = QgsRasterLayer(dataSource, baseName = name, 
                                    providerType = "wms")
    except TypeError as typo:
        rasterLayer = QgsRasterLayer(dataSource, baseName = name, 
                                    providerKey = "wms")
    finally:
        if rasterLayer is None: return None
    # QMessageBox.about(None, "create_raster_XYZ", 
    # "\n ".join([str(dataSource), str(rasterLayer)]))
            
    if rasterLayer.isValid():
        if not boundingRect is None:
            rasterLayer.setCrs(QgsCoordinateReferenceSystem(projection))
            rasterLayer.setExtent(boundingRect)
        return rasterLayer
    else:
        return None

def create_raster_file(url:str, name:str, additional_str:str = None, projection: str = "EPSG3857", boundingRect: QgsRectangle = None, zmin:int = 0, zmax:int = 18):
    data = url+additional_str
    png_path = dirname(__file__) + "/temp.png"
    tif_path = dirname(__file__) + "/temp.tif"
    load_url(data, png_path)
    breakthrough = False
    if not breakthrough:
        try:
            boundingbox = [boundingRect.xMinimum(), boundingRect.yMinimum(), boundingRect.xMaximum(), boundingRect.yMaximum()]
            breakthrough = True
        except AttributeError as exc:
            pass
    if not breakthrough:
        try:
            if len(boundingRect) == 4:
                boundingbox = boundingRect
                breakthrough = True
        except AttributeError as exc:
            pass
    if not breakthrough:
        return None
    
    projection = int(projection.replace("EPSG:", ""))
    # QMessageBox.about(None, "create_raster_XYZ", 
    # "\n ".join([str(data), str(boundingbox), str(projection)]))    
    georeference(png_path, tif_path, projection, boundingbox)
    rasterLayer = None
    try:
        rasterLayer = QgsRasterLayer(tif_path, baseName = name, 
                                    providerType = "gdal")
    except TypeError as typo:
        rasterLayer = QgsRasterLayer(tif_path, baseName = name, 
                                    providerKey = "gdal")
    finally:
        if rasterLayer is None: return None
    if rasterLayer.isValid():
        return rasterLayer
    else:
        return None
    

def create_layer(product: Product, tileservice: TileService, scene: Scene):
    # create new layer
    typeVar = ""
    url: str = ""
    name: str = str(product)
    boundingbox: List[float] = list()
    rasterLayer = None
    if tileservice is None:
        typeVar = "preview"
        url = scene.browseimage["EPSG:3857"].url
        rect: QgsRectangle = scene.bounding_shape.geometry.boundingBox()
        boundingbox = [rect.xMinimum(), rect.yMinimum(), rect.xMaximum(), rect.yMaximum()]
        crsSrc = QgsCoordinateReferenceSystem("EPSG:4326")    # WGS 84
        crsDest = QgsCoordinateReferenceSystem("EPSG:3857")  # Preudo-mercator
        transformContext = QgsProject.instance().transformContext()
        xform = QgsCoordinateTransform(crsSrc, crsDest, transformContext)
        boundingbox = [*xform.transform(boundingbox[0],boundingbox[1]), *xform.transform(boundingbox[2],boundingbox[3])]
        
        rasterLayer = create_raster_file(url, name, 
                            additional_str = APIKey().getRequestPart(), 
                            projection = "EPSG:3857", 
                            boundingRect = boundingbox, 
                            zmin = 0, zmax = 18)
    else:
        typeVar = "xyz"
        url = tileservice.url
        boundingbox = tileservice.bbox
        crsSrc = QgsCoordinateReferenceSystem("EPSG:4326")    # WGS 84
        crsDest = QgsCoordinateReferenceSystem("EPSG:3857")  # Preudo-mercator
        transformContext = QgsProject.instance().transformContext()
        xform = QgsCoordinateTransform(crsSrc, crsDest, transformContext)
        boundingbox = [*xform.transform(boundingbox[0],boundingbox[1]), *xform.transform(boundingbox[2],boundingbox[3])]
        rasterLayer = create_raster_XYZ(url, name, 
                            additional_str = APIKey().getRequestPart(), 
                            projection = "EPSG:3857", 
                            boundingRect = QgsRectangle(*boundingbox), 
                            zmin = tileservice.min_zoom, zmax = tileservice.max_zoom)
    return rasterLayer
 

if __name__ == "__main__":
    """
    type=xyz&url=https://bbp.ntsomz.ru/tile_services/server-1/Tiles/18591063/MM2_MSU102_20200417T084649_11900900/NDVI/{z}/{x}/{y}.png?api_key=MTg1OTAwMzk.MTg1OTAwNDU.84b0fd3f1b-94fcd8-3b01c4&zmax=11&zmin=0&crs=EPSG4326
    type=xyz&url=https://bbp.ntsomz.ru/tile_services/server-1/Tiles/18591063/MM2_MSU102_20200417T084649_11900900/NDVI/{z}/{x}/{y}.png&zmax=18&zmin=0&crs=EPSG3857
    type=xyz&url=https://bbp.ntsomz.ru/tile_services/server-1/Tiles/18591063/MM2_MSU102_20200417T084649_11900900/NDVI/{z}/{x}/{y}.png&zmax=11&zmin=0&crs=EPSG4326
    """
    bb = [39.552995, 49.404492, 48.192643, 54.477736]
    rect = QgsRectangle(QgsPointXY(bb[0], bb[1]), QgsPointXY(bb[2],bb[3]))
    data = "https://bbp.ntsomz.ru/api/v1/resources/browseimages/EPSG-3857/MM2_MSU101_20200421T054409_11900700"
    key_str = "?api_key=MTg1OTAwMzk.MTg1OTAwNDU.84b0fd3f1b-94fcd8-3b01c4"
    