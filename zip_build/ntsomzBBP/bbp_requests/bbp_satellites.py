import requests
import json
from typing import List
from ..params.setting import BBPSetting
from .debug import RUN_TYPE_DEBUG, debug_info_path
from os.path import dirname, join

class Sensor():
    def __init__(self, name = "", platform_id = ""):
        self.id = name
        self.satellite_id = platform_id
        self.__chosen__: bool = False

    def select(self):
        self.__chosen__ = True

    def deselect(self):
        self.__chosen__ = False

    def isSelected(self)->bool:
        return self.__chosen__
    
    def getHash(self)->str:
        return "{} : {}".format(str(self.satellite_id), str(self.id))

    def __str__(self)->str:
        return "{} : {} : ".format(str(self.satellite_id), str(self.id)) + ("Chosen" if self.__chosen__ else "Exempt")

class Satellite():
    def __init__(self, name = "", platform_id = "", sensors_ids = list(), description = dict(), *args, **kwargs):
        self.name:str = name
        self.id = platform_id
        self.sensors:List[Sensor] = [Sensor(i, self.id) for i in sensors_ids]
        self.description = description

    def __str__(self)->str:
        return json.dumps({
            "name": self.name,
            "platform_id": self.id,
            "sendors_ids": [str(i.id) for i in self.sensors],
            "description": self.description
        })

class Sattelites():

    __entities__:dict = dict()
    def __init__(self):
        self.__reqres = self.__getrequest__()
        self.__entities__ = self.__form_structures__()

    def __getrequest__(self)->str:
        api_location = BBPSetting().server
        api_key = BBPSetting().getRequestPart()

        reqbody = "/api/v1/resources/reference/platforms"
        req = api_location+reqbody+api_key
        print(req)
        p = debug_info_path("get_platforms.json")
        res = None
        if RUN_TYPE_DEBUG:
            debug_file = debug_info_path("debug_geometry.json")
            print(debug_file)
            with open(debug_file, "r", encoding = "utf-8") as f:
                text = f.read()
                res = json.loads(text)
        else:
            res = requests.get(req)
            print(res)
            if res.status_code == 200:
                print("Request fulfilled")
                con = res.text
                with open(p, "w") as f:
                    f.write(con)
                res = json.loads(con)
            elif res.status_code == 500:
                print("Request failed")
                con = res.text
                print(con)
                with open(p, "w") as f:
                    f.write(con)
                res = None
        return res

    def __form_structures__(self):
        if not self.__reqres is None:
            result = self.__reqres["result"]
            return [Satellite(**i) for i in result]
        else:
            return dict()

    def getSatellites(self):
        return self.__entities__

    def getSensors(self):
        return [j for i in self.__entities__ for j in i.sensors]

if __name__ == "__main__":
    s = Sattelites()
    for i in s.getSatellites():
        print(i)
    for i in s.getSensors():
        print(i)
