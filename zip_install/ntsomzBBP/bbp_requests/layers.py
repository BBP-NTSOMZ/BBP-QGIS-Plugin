from qgis.core import (
  QgsApplication,
  QgsDataSourceUri,
  QgsCategorizedSymbolRenderer,
  QgsClassificationRange,
  QgsPointXY,
  QgsProject,
  QgsExpression,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsFeatureIterator,
  QgsFeatureRequest,
  QgsFeatureRenderer,
  QgsGeometry,
  QgsGraduatedSymbolRenderer,
  QgsMarkerSymbol,
  QgsMessageLog,
  QgsRectangle,
  QgsRendererCategory,
  QgsRendererRange,
  QgsSymbol,
  QgsVectorDataProvider,
  QgsVectorLayer,
  QgsVectorFileWriter,
  QgsWkbTypes,
  QgsSpatialIndex,
)

from qgis.core.additions.edit import edit
from qgis.PyQt.QtCore import (
    QVariant
)
from qgis.PyQt.QtGui import (
    QColor,
)

from bbp_requests import geometry

def JSONGeometryFromLayer(qgsLayer: QgsVectorLayer)->str:
    features: QgsFeatureIterator = qgsLayer.getFeatures()
    geomType: QgsWkbTypes.GeometryType = qgsLayer.geometryType()
    ret_geom = None
    for feature in features:
        geom:QgsGeometry = QgsGeometry(feature.geometry())
        if ret_geom is None:
            if geomType == QgsWkbTypes.Polygon:
                ret_geom = geom.asMultiPolygon()
            if geomType == QgsWkbTypes.MultiPolygon:
                ret_geom = geom
        if geomType == QgsWkbTypes.Polygon:
            ret_geom.addPartGeometry(geom)
        elif geomType == QgsWkbTypes.MultiPolygon:
            for i in geom.parts():
                ret_geom.addPartGeometry(i)
    return geometry.QgsGeometrytoGeoJSON(ret_geom) 

def fieldFromDict(dictionary:dict, keyname:str, valueType: QVariant)->QgsField:
    value = dictionary.get(keyname)
    if value is None:
        return None
    field = QgsField(keyname, valueType)

def layerFromFeature(geom: str, feature_json: dict):
    geom = geometry.GeoJSONtoQgsGeomentry(geom)
    fields = QgsFields()
    for key,value in feature_json.items():
        fields.append(QgsField(key, QVariant.S))
    vl = QgsVectorLayer()
