from os import environ
import shelve

class Config():
    
    def __init__(self, env = None):
        app_env = environ['APP_ENV'] if env is None else env 
        d = shelve.open("config.shl")
        for key in d.get("general").keys():
            if d.get(app_env) and d.get(app_env).has_key(key):
                setattr(self, key, d.get(app_env).get(key))
            else:
                setattr(self, key, d.get("general").get(key))
        d.close()
        
