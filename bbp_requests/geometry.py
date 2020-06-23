import json
from typing import Union,List
from osgeo import ogr
from os.path import join, dirname
from qgis.core import (
  QgsGeometry,
  QgsPoint,
  QgsPointXY,
  QgsWkbTypes,
  QgsProject,
  QgsFeatureRequest,
  QgsVectorLayer,
  QgsDistanceArea,
  QgsUnitTypes,
  QgsJsonUtils
)

def GeoJSONtoQgsGeomentry(_json:Union[dict,str])->QgsGeometry:
    if isinstance(_json, dict):
        _json = json.dumps(_json)
    ret = ogr.CreateGeometryFromJson(_json)
    return QgsGeometry.fromWkt(ret.ExportToWkt())

def QgsGeometrytoGeoJSON(geom: QgsGeometry)->str:
    ret = geom.asJson()
    return ret

def __testCall():
    data = None
    DEBUG = True
    if DEBUG:
        loc_dir = dirname(__file__)
        debug_file = join(loc_dir,"debug_geometry.json")
        print(debug_file)
        with open(debug_file, "r", encoding = "utf-8") as f:
            data = f.read()
            di = json.loads(data)
            data = json.dumps(di["geometry"])
    ret = GeoJSONtoQgsGeomentry(data)
    return ret

def __testCall2(geom):
    print(QgsGeometrytoGeoJSON(geom))    

if __name__ == "__main__":
    s = __testCall()
    print(s)
    __testCall2(s)
