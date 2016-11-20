from os import environ

try:
    environ["APP_ENV"]
except KeyError:
    environ["APP_ENV"] = "local"