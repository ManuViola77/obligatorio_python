import shelve
d = shelve.open("config.shl")

d["general"] = {"dbhost":"localhost","dbuser":"root","dbpasswd":"","db":"obligatorio"}

d["local"] = {"dbhost":"localhost","dbuser":"root","dbpasswd":"","db":"obligatorio"}

d.close()

from Lib.Extra.Config import Config
Conf = Config()

#print Conf.dbuser