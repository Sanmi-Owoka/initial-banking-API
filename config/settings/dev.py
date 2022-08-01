from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

BCC_EMAIL = env.list("BCC_EMAIL")