from typing import List, Union, Optional
from datetime import datetime
from os.path import dirname, join
from . import geometry
from .bbp_objects import Scene, BrowseImage, BoundingShape
# import bbp_key
# import geometry
import requests
import json

class MinMaxLimits():
    def __init__(self,_min, _max):
        self.min = _min
        self.max = _max

class SearchResults():
    def __init__(self, request, first_result):
        self.req = request
        self.last_res = first_result
        self.curPage = first_result["current_page"]

    def getNextPage(self):
        if not self.last_res is None:
            total_entries = self.last_res["total_entries"]
            last_page = self.last_res["last_page"]
            current_page = self.last_res["current_page"]
            if last_page > current_page:
                self.req.setPage(current_page + 1)
                new_way = self.req.search()
                self.last_res = new_way.last_res
                self.curPage += 1
                return self.result()
            else:
                return None

    def result(self):
        res = self.last_res["result"]
        return [Scene(**i) for i in res]

class requestSearch():
    """
    Атрибуты поискового запроса
        acquisition_date
        available_to_order_only
        geometry_object
        geometry_relation
        catalogization_date
        cloud_cover
        platform_id
        products
        resolution
        scene_id
        sensor_id
        sensor_azimuth_angle
        sensor_zenith_angle
        sun_azimuth_angle
        sun_zenith_angle
        sun_zenith_angle
        fields
        page
        items
        sort
    """

    acquisition_date: Optional[List[MinMaxLimits]] = list()
    available_to_order_only: Optional[bool] = False
    geometry_object: Optional[dict] = dict()
    geometry_relation: Optional[str] = "within"
    catalogization_date: Optional[List[MinMaxLimits]] = list()
    cloud_cover: Optional[MinMaxLimits] = MinMaxLimits(0,100)
    platform_id: Optional[List[str]] = list()
    products: Optional[List[str]] = list()
    resolution: Optional[List[str]] = list()
    scene_id: Optional[List[str]] = list()
    sensor_id: Optional[List[str]] = list()
    sensor_azimuth_angle: Optional[List[MinMaxLimits]] = list()
    sensor_zenith_angle: Optional[List[MinMaxLimits]] = list()
    sun_azimuth_angle: Optional[List[MinMaxLimits]] = list()
    sun_zenith_angle: Optional[List[MinMaxLimits]] = list()
    fields: Optional[List[str]] = list()
    page:int = 1
    items:int = 100
    sort:Optional[List[dict]] = list()

    def __init__(self,
                acquisition_date: Optional[List[MinMaxLimits]] = None,
                available_to_order_only: Optional[bool] =  None,
                geometry_object: Optional[dict] =  None,
                geometry_relation: Optional[str] = None,
                catalogization_date: Optional[List[MinMaxLimits]] = None,
                cloud_cover: Optional[MinMaxLimits] =  None,
                platform_id: Optional[List[str]] = None,
                products: Optional[List[str]] = None,
                resolution: Optional[List[str]] = None,
                scene_id: Optional[List[str]] =  None,
                sensor_id: Optional[List[str]] =  None,
                sensor_azimuth_angle: Optional[List[MinMaxLimits]] =  None,
                sensor_zenith_angle: Optional[List[MinMaxLimits]] = None,
                sun_azimuth_angle: Optional[List[MinMaxLimits]] =  None,
                sun_zenith_angle: Optional[List[MinMaxLimits]] =  None,
                fields: Optional[List[str]] =  None,
                page:Optional[int] = None,
                items:Optional[int] = None,
                sort:Optional[List[dict]] = None,
                **kwargs):
        self.acquisition_date = acquisition_date
        self.available_to_order_only = available_to_order_only
        self.geometry_object = geometry_object
        self.geometry_relation = geometry_relation
        self.catalogization_date = catalogization_date
        self.cloud_cover = cloud_cover
        self.platform_id = platform_id
        self.products = products
        self.resolution = resolution
        self.scene_id = scene_id
        self.sensor_id = sensor_id
        self.sensor_azimuth_angle = sensor_azimuth_angle
        self.sensor_zenith_angle = sensor_zenith_angle
        self.sun_azimuth_angle = sun_azimuth_angle
        self.sun_zenith_angle = sun_zenith_angle
        self.fields = fields
        self.page = page
        self.items = items
        self.sort = sort

    def addAcquisitionDate(self, dateFrom: datetime, dateTill: datetime):
        if self.acquisition_date is None:
            self.acquisition_date = list()
        self.acquisition_date.append(MinMaxLimits(dateFrom, dateTill))

    def addGeometryObject(self, geoJSON:dict):
        self.geometry_object = geoJSON

    def setCloudCover(self, _min: float, _max: float):
        self.cloud_cover = MinMaxLimits(_min, _max)

    def addPlatformID(self, ids: Union[List[str], str]):
        if isinstance(ids, list):
            for i in ids:
                self.platform_id.append(i)
        elif isinstance(ids, str):
            self.platform_id.append(ids)

    def addProducts(self, ids: Union[List[str], str]):
        if isinstance(ids, list):
            if self.products is None:
                self.products = ids
            else:
                self.products += ids
            
        elif isinstance(ids, str):
            if self.products is None:
                self.products = [ids]
            else:
                self.products.append(ids)

    def setResolution(self, res: Union[List[str],str]):
        if isinstance(res, list):
            self.products = res
        elif isinstance(res, str):
            self.products.append(res)

    def addSceneID(self, ids: Union[List[str], str]):
        if isinstance(ids, list):
            if self.scene_id is None:
                self.scene_id = ids
            else:
                self.scene_id += ids
        elif isinstance(ids, str):
            if self.scene_id is None:
                self.scene_id = [ids]
            else:
                self.scene_id.append(ids)

    def addSensorID(self, ids: List[str]):
        if self.sensor_id is None:
            self.sensor_id = list()
        self.sensor_id = self.sensor_id + ids

    def addSensorAzimuthAngle(self, azimuth: List[MinMaxLimits]):
        self.sensor_azimuth_angle = self.sensor_azimuth_angle + azimuth

    def addSensorZenithAngle(self, zenith: List[MinMaxLimits]):
        self.sensor_zenith_angle = self.sensor_zenith_angle + zenith
    
    def addSunAzimuthAngle(self, azimuth: List[MinMaxLimits]):
        self.sun_azimuth_angle = self.sun_azimuth_angle + azimuth
    
    def addSunZenithAngle(self, zenith: List[MinMaxLimits]):
        self.sun_zenith_angle = self.sun_zenith_angle + zenith

    def setFields(self, fields:List[str]):
        self.fields = fields

    def setPage(self, page:int):
        self.page = page

    def setItems(self, items: int):
        self.items = items
    
    def setSort(self, sort:List[dict]):
        self.sort = sort

    def __request__acquisition_date__(self)->dict:
        if not self.acquisition_date is None:
            ret = {"acquisition_date": 
                [[i.min.isoformat(sep="T"),i.max.isoformat(sep="T")] for i in self.acquisition_date]
            }
            return ret
        return None

    def __request__available_to_order_only(self)->dict:
        if not self.available_to_order_only is None:
            return {"available_to_order_only": self.available_to_order_only}
        return None

    def __request__geometry_object__(self)->dict:
        if not self.geometry_object is None:
            return {"geometry_object": self.geometry_object}

    def __request__geometry_relation__(self)->dict:
        if not self.geometry_object is None:
            return {"geometry_relation":self.geometry_relation}

    def __request__cloud_cover__(self)->dict:
        if not self.cloud_cover is None:
            return {"cloud_cover":[self.cloud_cover.min, self.cloud_cover.max]}

    def __request__platform_id__(self)->dict:
        if not self.platform_id is None:
            return {"platform_id": self.platform_id}
    
    def __request__products__(self)->dict:
        if not self.products is None:
            return {"products": self.products}

    def __request__resolution__(self)->dict:
        if not self.resolution is None:
            return {"resolution": self.resolution}

    def __request__scene_id__(self)->dict:
        if not self.scene_id is None:
            return {"scene_id": self.scene_id}

    def __request__sensor_id__(self)->dict:
        if not self.sensor_id is None:
            return {"sensor_id": self.sensor_id}

    def __request__sensor_azimuth_angle__(self)->dict:
        if not self.sensor_azimuth_angle is None:
            return {"sensor_azimuth_angle": [[self.sensor_azimuth_angle.min, self.sensor_azimuth_angle.max] for i in self.sensor_azimuth_angle]}

    def __request__sensor_zenith_angle__(self)->dict:
        if not self.sensor_zenith_angle is None:
            return {"sensor_zenith_angle": [[self.sensor_zenith_angle.min, self.sensor_zenith_angle.max] for i in self.sensor_zenith_angle]}

    def __request__sun_azimuth_angle__(self)->dict:
        if not self.sun_azimuth_angle is None:
            return {"sun_azimuth_angle": [[self.sun_azimuth_angle.min, self.sun_azimuth_angle.max] for i in self.sun_azimuth_angle]}

    def __request__sun_zenith_angle__(self)->dict:
        if not self.sun_zenith_angle is None:
            return {"sun_zenith_angle": [[self.sun_zenith_angle.min, self.sun_zenith_angle.max] for i in self.sun_azimuth_angle]}

    def __request__fields__(self)->dict:
        if not self.fields is None:
            return {"fields": self.fields}
    
    def __request__page__(self)->dict:
        if not self.page is None:
            return {"page": self.page}
    
    def __request__items__(self)->dict:
        if not self.items is None:
            return {"items": self.items}

    def __request__sort__(self)->dict:
        if not self.sort is None:
            return {"sort": self.sort}
    
    def __request__(self):
        r = [
            self.__request__acquisition_date__,
            self.__request__available_to_order_only,
            self.__request__cloud_cover__,
            self.__request__fields__,
            self.__request__geometry_object__,
            self.__request__geometry_relation__,
            self.__request__items__,
            self.__request__page__,
            self.__request__platform_id__,
            self.__request__products__,
            self.__request__resolution__,
            self.__request__scene_id__,
            self.__request__sensor_azimuth_angle__,
            self.__request__sensor_id__,
            self.__request__sensor_zenith_angle__,
            self.__request__sort__,
            self.__request__sun_azimuth_angle__,
            self.__request__sun_zenith_angle__
        ]
        r = [i() for i in r]
        r = [i for i in r if not i is None]
        req = {key: value for i in r for key, value in i.items()}
        return req

    def __str__(self)->str:
        ret = json.dumps(self.__request__(), indent = 4)
        return ret

    def __postrequest__(self):
        api_location = BBPSetting().server
        api_key = BBPSetting().getRequestPart()

        reqbody = "/api/v1/resources/scenes"
        reqdata = self.__request__()
        p = join(dirname(__file__),"send_search.json")
        with open(p,"w") as f:
            f.write(str(self))
        req = api_location+reqbody+api_key
        p = join(dirname(__file__),"post_search.json")
        res = requests.post(req, json = reqdata)
        con = res.text
        with open(p, "w") as f:
            f.write(con)
        if res.status_code == 200:
            res = json.loads(con)
        elif res.status_code == 500:
            res = None
        return res

    def search(self):
        result = self.__postrequest__()
        if not result is None:
            items = result["result"]
            print(len(items))
            res = SearchResults(self, result)
            return res
            
def search_scene(sceneID, product)->Scene:
    t = requestSearch()
    # t.setFields([
    # "products",
    # "sensor_id",
    # "bands",
    # "browseimage",
    # "bounding_shape",
    # "scene_id",
    # "catalogization_date",
    # "available_to_order"
    # ])
    t.addAcquisitionDate(datetime(2000,4,1,0,0,0), datetime.now())
    t.addSceneID(sceneID)
    t.addProducts(product)
    res = t.search()
    loads = res.result()
    while not loads is None:
        for i in loads:
            return i
        break
        loads = res.getNextPage()
        


if __name__ == "__main__":
    t = requestSearch()
    t.setCloudCover(40,100)
    t.addAcquisitionDate(datetime(2000,4,1,0,0,0), datetime.now())
    
    t.addSensorID(["MSU101",
    "MSU102"])
    t.setFields([
    "products",
    "sensor_id",
    "bands",
    "browseimage",
    "bounding_shape",
    "scene_id",
    "catalogization_date",
    "available_to_order"
    ])
    t.addSceneID(["MM2_MSU101_20200421T054629_11900900"])
    t.addProducts(["TOAL"])
    print(t)
    res = t.search()
    loads = res.result()
    var = 0
    j = 0
    while not loads is None:
        j += 1
        for i in loads:
           var += 1
           print(var)
        loads = res.getNextPage()