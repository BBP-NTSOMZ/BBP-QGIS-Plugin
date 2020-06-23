from typing import List, Optional

attr_key = "?api_key="
key = "MTg1OTAwMzk.MTg1OTAwNDU.84b0fd3f1b-94fcd8-3b01c4"

class APIKey:
    class __StaticInstant__:
        def __init__(self, key: Optional[str] = None):
            self.key = key

        def __str__(self):
            return repr(self) + self.key
            
    instance = None

    def __init__(self, key: Optional[str] = None):
        if not key is None:
            self.setAPIKey(key)

    @classmethod
    def __create_instance__(cls):
        if cls.instance is None:
            cls.instance = cls.__StaticInstant__()

    def setAPIKey(self, key:str):
        APIKey.__create_instance__()
        APIKey.instance.key = key

    def getRequestPart(self)->str:
        if APIKey.instance is None:
            return None
        ret = attr_key+APIKey.instance.key
        return ret

    def __bool__(self)->bool:
        if not APIKey.instance is None:
            return True
        return False

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self)->str:
        return APIKey.instance.key

APIKey().setAPIKey(key)