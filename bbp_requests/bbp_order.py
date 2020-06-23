from typing import List, Union, Optional, Any
from .bbp_key import APIKey, key, attr_key
from .bbp_objects import Order, Product, TileService, Point
#from dataclasses import dataclass,field
from datetime import datetime
from os.path import dirname, join
import requests
import json



#@dataclass
class requestOrders():
    """
    Параметры URL-строки поискового запроса
        completed_start - String / Number - Задает начальное время интервала для ограничения результирующего набора данных по значению атрибута заказа completed
        completed_end   - String / Number - Задает конечное время интервала для ограничения результирующего набора данных по значению атрибута заказа completed
        created_start   - String / Number - Задает начальное время интерваладля ограничения результирующего набора данных по значению атрибута заказа created
        created_end     - String / Number - Задает конечное время интерваладля ограничения результирующего набора данных по значению атрибута заказа created
        expires_start   - String / Number - Задает начальное время интерваладля ограничения результирующего набора данных по значению атрибута заказа expires
        expires_end     - String / Number - Задает конечное время интерваладля ограничения результирующего набора данных по значению атрибута заказа expires
        id              - Number - Ограничивает результирующий набор данных до заданных значений id заказа
        pointer         - String - Ограничивает результирующий набор данных до заданных значений pointer заказа
        responsive_id   - String - Ограничивает результирующий набор данных до заданных значений responsive_id заказа
        source          - String - Ограничивает результирующий набор данных до заданных значений source. Возможны следующие значения: API	для заказов, сформированных через API; UI	для заказов, сформированных через пользовательский интерфейс
        state           - String - Ограничивает результирующий набор данных до заданных значений состояний source заказов. возможны следующие значения: created	для созданного заказа: processing - для созданного заказа; completed - для успешно завершенного заказа; expired	- для заказа, время жизни которого истекло;
        page            - Number - Определяет страницу результирующего набора
        items           - Number - Определяет количество совпадений на одну страницу. Максимальное значение 300
        sort            - Array of Strings - Определяет порядок сортировки. Следующие  атрибуты заказа   могут быть использованы для сортировки результирующего набора:  created,  completed,  expires,  state,  id,  responsive_id,  pointer,  
    """
    
    completed_start: Optional[Union[str, int]] = None
    completed_end: Optional[Union[str, int]] = None
    created_start: Optional[Union[str, int]] = None
    created_end: Optional[Union[str, int]] = None
    expires_start: Optional[Union[str, int]] = None
    expires_end: Optional[Union[str, int]] = None
    id: Optional[int] = None
    pointer: Optional[str] = None
    responsive_id: Optional[str] = None
    source: Optional[str] = None
    state: Optional[str] = None
    page: Optional[int] = None
    items: Optional[int] = None
    sort: Optional[List[str]] = list()

    def __init__(self,
    completed_start : Optional[Union[str, int]] = None,
    completed_end   : Optional[Union[str, int]] = None,
    created_start   : Optional[Union[str, int]] = None,
    created_end     : Optional[Union[str, int]] = None,
    expires_start   : Optional[Union[str, int]] = None,
    expires_end     : Optional[Union[str, int]] = None,
    id              : Optional[int] = None,
    pointer         : Optional[str] = None,
    responsive_id   : Optional[str] = None,
    source          : Optional[str] = None,
    state           : Optional[str] = None,
    page            : Optional[int] = None,
    items           : Optional[int] = None,
    sort            : Optional[List[str]] = list() ):
        self.completed_start = completed_start 
        self.completed_end   = completed_end   
        self.created_start   = created_start   
        self.created_end     = created_end     
        self.expires_start   = expires_start   
        self.expires_end     = expires_end     
        self.id              = id              
        self.pointer         = pointer         
        self.responsive_id   = responsive_id   
        self.source          = source          
        self.state           = state           
        self.page            = page            
        self.items           = items           
        self.sort            = sort            

    def __request__(self):
        api_location = "https://bbp.ntsomz.ru"
        reqbody = "/api/v1/resources/orders"
        reqkey = APIKey().getRequestPart()
        req = api_location+reqbody+reqkey
        p = dirname(__file__)
        p = join(p,"get_orders.json")
        res = requests.get(req)
        if res.status_code == 200:
            print("Request fulfilled 200")
            con = res.text
            with open(p, "w") as f:
                f.write(con)
            res = json.loads(con)
            self.__last_req = res
        elif res.status_code == 500:
            print("Request failed 500")
            con = res.text
            print(con)
            with open(p, "w") as f:
                f.write(con)
            res = None
        else:
            con = res.text
            print(con)
            with open(p, "w") as f:
                f.write(con)
            res = None
        return res

    def getOrders(self):
        req = self.__request__()
        if req is None:
            return None            
        return [Order(**i) for i in req["result"]]
            

if __name__ == "__main__":
    reqord = requestOrders()
    orders = reqord.getOrders()
    products = [j for i in orders for j in i.getProducts()]
    print(products)
