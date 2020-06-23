from typing import List, Union, Any, Dict, Optional
#from dataclasses import dataclass,field, InitVar
from datetime import datetime
from .geometry import GeoJSONtoQgsGeomentry, QgsGeometrytoGeoJSON

#@dataclass
class BoundingShape():

    type: str
    geometry: Union[dict, "QgsGeometry"] = dict()

    def __init__(self, type: str, geometry: dict):
        self.type = type
        if isinstance(geometry, dict):
            self.geometry = geometry
        self.__post_init__()

    def __post_init__(self):
        self.geometry = GeoJSONtoQgsGeomentry(self.geometry)

#@dataclass
class BrowseImage():
    projection:str
    url: str

    def __init__(self, projection: str, url: dict):
        self.projection = projection
        self.url = url

#@dataclass
class Scene():
    """
    acquisition_date
    acquisition_date_start
    acquisition_date_stop
    available_to_order
    bands
    bands_names
    bounding_shape
    browseimage
    catalogization_date
    cloud_cover
    composite_sensors
    frame
    orbit_pass
    orbit_pass_direction
    platform_id
    products
    resolution
    L
    M
    H
    route	
    scene_id	
    sensor_id	
    sensor_azimuth_angle	
    sensor_zenith_angle	
    sun_azimuth_angle
    sun_zenith_angle
    """
    
    acquisition_date: Optional[Union[str,datetime]] = None
    acquisition_date_start: Optional[Union[str,datetime]] = None
    acquisition_date_stop: Optional[Union[str,datetime]] = None
    available_to_order:bool = True 
    bands: List[str] = list()
    bands_names: List[str] = list()
    bounding_shape: Dict[str, Any] = dict()
    browseimage: Dict[str, Union[str,BrowseImage]] = dict()
    catalogization_date: Optional[Union[str,datetime]] = None
    cloud_cover: Optional[float] = None
    composite_sensors: Dict[str, List[str]] = dict()
    deleted: bool = False
    frame: Optional[int] = None
    modification_date: Optional[Union[str,datetime]] = None
    orbit_pass: Optional[int] = None
    orbit_pass_direction: Optional[str] = None
    platform_id: Optional[str] = None
    processing_level: Optional[str] = None
    processing_level_classification: Optional[str] = None
    products: List[str] = list()
    resolution: Optional[str] = None
    route: Optional[int] = None
    scene_id: Optional[str] = None
    sensor_azimuth_angle: Optional[float] = None
    sensor_id: Optional[str] = None
    sensor_zenith_angle: Optional[float] = None	
    sun_azimuth_angle: Optional[float] = None
    sun_zenith_angle: Optional[float] = None

    def __init__(self,
    acquisition_date: Optional[Union[str,datetime]] = None,
    acquisition_date_start: Optional[Union[str,datetime]] = None,
    acquisition_date_stop: Optional[Union[str,datetime]] = None,
    available_to_order:bool = True ,
    bands: List[str] = list(),
    bands_names: List[str] = list(),
    bounding_shape: Dict[str, Any] = dict(),
    browseimage: Dict[str, Union[str,BrowseImage]] = dict(),
    catalogization_date: Optional[Union[str,datetime]] = None,
    cloud_cover: Optional[float] = None,
    composite_sensors: Dict[str, List[str]] = dict(),
    deleted: bool = False,
    frame: Optional[int] = None,
    modification_date: Optional[Union[str,datetime]] = None,
    orbit_pass: Optional[int] = None,
    orbit_pass_direction: Optional[str] = None,
    platform_id: Optional[str] = None,
    processing_level: Optional[str] = None,
    processing_level_classification: Optional[str] = None,
    products: List[str] = list(),
    resolution: Optional[str] = None,
    route: Optional[int] = None,
    scene_id: Optional[str] = None,
    sensor_azimuth_angle: Optional[float] = None,
    sensor_id: Optional[str] = None,
    sensor_zenith_angle: Optional[float] = None	,
    sun_azimuth_angle: Optional[float] = None,
    sun_zenith_angle: Optional[float] = None):
        self.acquisition_date                = acquisition_date               
        self.acquisition_date_start          = acquisition_date_start         
        self.acquisition_date_stop           = acquisition_date_stop          
        self.available_to_order              = available_to_order             
        self.bands                           = bands                          
        self.bands_names                     = bands_names                    
        self.bounding_shape                  = bounding_shape                 
        self.browseimage                     = browseimage                    
        self.catalogization_date             = catalogization_date            
        self.cloud_cover                     = cloud_cover                    
        self.composite_sensors               = composite_sensors              
        self.deleted                         = deleted                        
        self.frame                           = frame                          
        self.modification_date               = modification_date              
        self.orbit_pass                      = orbit_pass                     
        self.orbit_pass_direction            = orbit_pass_direction           
        self.platform_id                     = platform_id                    
        self.processing_level                = processing_level               
        self.processing_level_classification = processing_level_classification
        self.products                        = products                       
        self.resolution                      = resolution                     
        self.route                           = route                          
        self.scene_id                        = scene_id                       
        self.sensor_azimuth_angle            = sensor_azimuth_angle           
        self.sensor_id                       = sensor_id                      
        self.sensor_zenith_angle             = sensor_zenith_angle            
        self.sun_azimuth_angle               = sun_azimuth_angle              
        self.sun_zenith_angle                = sun_zenith_angle     
        self.__post_init__()          

    def __post_init__(self):
        if not self.bounding_shape is None:
            self.bounding_shape = BoundingShape(**self.bounding_shape)
        if not self.browseimage is None:
            self.browseimage = {key: BrowseImage(key, value) for key, value in self.browseimage.items()}
        


#@dataclass
class Point():
    lat: float
    lon: float
    elevation: float = 0.0

    def __init__(self,
    lat: float,
    lon: float,
    elevation: float = 0.0):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation


#@dataclass
class TileService():
    """
    url
    bbox
    min_zoom
    max_zoom
    color_representation
    """
    url: str
    bbox: List[float] = list()
    min_zoom: int = 0
    max_zoom: int = 18
    color_representation: Optional[Any] = None
    
    def __init__(self,
    url: str,
    bbox: List[float] = list(),
    min_zoom: int = 0,
    max_zoom: int = 18,
    color_representation: Optional[Any] = None,
    ):
        self.url                    = url                 
        self.bbox                   = bbox                
        self.min_zoom               = min_zoom            
        self.max_zoom               = max_zoom            
        self.color_representation   = color_representation

    def getBoundingRect(self)->(Point, Point):
        ilen = len(self.bbox)
        dimentions = ilen/2
        if dimentions == 2:
            return (Point(self.bbox[0], self.bbox[1]), Point(self.bbox[2], self.bbox[3]))
        if dimentions == 3:
            return (Point(self.bbox[0], self.bbox[1], self.bbox[2]), Point(self.bbox[3], self.bbox[4], self.bbox[5]))

#@dataclass
class Product():
    """
    id           - String - Индетификатор сцены
    product      - String - Индетификатор продукта
    tile_service - Object - 
    """
    id:str
    product: str
    tile_service: TileService = None
    parent: "Order" = None

    def __init__(self,
    id:str,
    product: str,
    tile_service: TileService = None,
    parent: "Order" = None
    ):
        self.id             = id           
        self.product        = product      
        self.tile_service   = tile_service 
        self.parent         = parent       
        self.__post_init__()

    def __post_init__(self):
        if isinstance(self.tile_service, dict):
            self.tile_service = TileService(**self.tile_service)

    def __str__(self):
        return ": ".join((self.id, self.product))

#@dataclass()
class Order():
    """
    archive_structure   - Number - Код структуры файлов готового заказа, возможны следующие занчения: 1  единый архив для всего заказа
    completed           - String / Number - Время завершения обработки заказа
    composites          - Object / Null - Определяет состав заказа в части композитных изображений
    created             - String / Number - Время регистрации заказа
    download            - Object / Null - Определяет ссылки на файлы архивов и их размер для выполненного заказа. Структура объекта зависит от значения атрибута archive_structure
    expires	            - String / Number - Время, при наступлении которого заказ перестает быть доступным для получения. По умолчанию время жизни заказа составляет 1 сутки с момента завершения его подготовки
    id                  - Number - Идентификатор заказа
    pointer             - String / Null - Указатель
    products            - Object / Null - Определяет состав заказа в части стандартных и базовых продуктов
    responsive_id       - String - Идентификатор вида YYYYMMDD-n, где n -- порядковый номер заказа за соответствующую дату
    source              - String - Источник регистрации заказа. Возможны 2 значения: API или UI, для заказов, созданных через программный интерфейс или графический соответственно
    state               - String - Состояние (статус) заказа, возможны следующие значения: created - для созданного заказа; processing - статус указывает на инициализацию обработки заказа; completed - заказ успешно завершен; expired - время "жизни" заказа истекло;
    tile_services       - Object - Определяет параметры тайловых представлений (сервисов), подготовленных в рамках выполнения заказа
    """
    archive_structure: Optional[int] = None
    completed: Optional[Union[str,int]] = None    
    composites: Optional[dict] = dict() 
    created: Optional[Union[str,int]] = None
    download: Optional[dict] = dict() 
    expires: Optional[Union[str,int]] = None
    id: Optional[int] = None          
    pointer: Optional[str] = None           
    products: Optional[dict] = dict() 
    responsive_id: Optional[str] = None      
    source: Optional[str] = None          
    state: Optional[str] = None             
    tile_services: Optional[dict] = dict() 

    def __init__(self,
    archive_structure: Optional[int] = None,
    completed: Optional[Union[str,int]] = None,
    composites: Optional[dict] = dict(),
    created: Optional[Union[str,int]] = None,
    download: Optional[dict] = dict(),
    expires: Optional[Union[str,int]] = None,
    id: Optional[int] = None,
    pointer: Optional[str] = None,
    products: Optional[dict] = dict(),
    responsive_id: Optional[str] = None,
    source: Optional[str] = None,
    state: Optional[str] = None,
    tile_services: Optional[dict] = dict()
    ):  
        self.archive_structure  = archive_structure
        self.completed          = completed        
        self.composites         = composites       
        self.created            = created          
        self.download           = download         
        self.expires            = expires          
        self.id                 = id               
        self.pointer            = pointer          
        self.products           = products         
        self.responsive_id      = responsive_id    
        self.source             = source           
        self.state              = state            
        self.tile_services      = tile_services    


    def getProducts(self)->List[Product]:
        ret = None
        try:
            subret = [Product(id_key, product_key) for id_key, product_vals in self.products.items()]
            ret = [Product(id_key, product_key) for id_key, product_vals in self.products.items() for product_key, prod_val in product_vals.items()]
        except AttributeError as exc:
            return list()
        if not self.tile_services is None:
            tsp = self.tile_services.get("products")
            if not tsp is None:
                for index, prod in enumerate(ret):
                    tile_products = tsp.get(prod.id)
                    if tile_products is None: continue
                    tile_product = tile_products.get(prod.product)
                    if tile_product is None: continue
                    ret[index] = Product(prod.id, prod.product, tile_product, parent = self)
        return ret