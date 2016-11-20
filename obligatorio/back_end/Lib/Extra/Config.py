from os import environ
import shelve

class Config():
    
    def __init__(self, env = None):
        if env is None:
            app_env = environ["APP_ENV"]
        else:
            app_env = env    
        d = shelve.open("config.shl")
        for key in d.get("general").keys():
            if d.get(app_env).has_key(key):
                setattr(self,key,d.get(app_env).get(key))
            else:
                setattr(self, key, d.get("general").get(key))
        d.close()