from dataclasses import dataclass, field
from typing import Optional, List
from os.path import dirname, join
import json

class BBPSetting:

    __key_prefix__ = "?api_key="
    @dataclass
    class __StaticInstant__:

        key: str = field(default = str)
        server: str = field(default = "https://bbp.ntsomz.ru")

        def __post_init__(self):
            print("post_init", self.key, self.server)
            #self.key: str = key
            if self.server is None or not isinstance(self.server, str):
                self.server: str = "https://bbp.ntsomz.ru"
        
        @classmethod
        def load(cls,path):
            with open(path, "r") as f:
                data = json.load(f)
                print(data)
                data = cls(**data)
                print(data)
                f.close()
                return data
        
        def save(self, path):
            dick = dict()
            if not self.key is None:
                dick["key"] = self.key
            if not self.server is None:
                dick["server"] = self.server
            print("save", self)
            with open(path, "w") as f:
                json.dump(dick, f)
                f.close()
                
    instance = None
    name = "settings.json"

    def __init__(self):
        if BBPSetting.instance is None:
            BBPSetting.__create_instance__()

    @classmethod
    def __create_instance__(cls):
        if cls.instance is None:
            loc_dir = dirname(__file__)
            path_to_settings = join(loc_dir, cls.name)
            cls.instance = cls.__StaticInstant__.load(path_to_settings)

    def setAPIKey(self, key:str):
        BBPSetting.__create_instance__()
        loc_dir = dirname(__file__)
        path_to_settings = join(loc_dir, self.name)
        BBPSetting.instance.key = key
        print(path_to_settings, key)
        BBPSetting.instance.save(path_to_settings)

    def getRequestPart(self)->str:
        if BBPSetting.instance is None:
            return None
        ret = BBPSetting.__key_prefix__+BBPSetting.instance.key
        return ret

    def __bool__(self)->bool:
        if not BBPSetting.instance is None:
            return True
        return False

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self)->str:
        return BBPSetting.instance.key
