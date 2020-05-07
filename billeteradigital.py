#Para ejecutar se utiliza> python BilletaraDigital.py  (desde la consola)
#Las cotizaciones se procesan y actualizan al principio de la aplicación para todas las monedas de la lista
import random
from requests import Request, session
from requests.exceptions import ConnectionError, Timeout
import json
from datetime import datetime


