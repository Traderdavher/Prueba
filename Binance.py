import Configuracion
import requests
import json
import hmac
import hashlib
from datetime import datetime

class Binance:
    apiKey = ""
    secretKey = ""
    url = ""
    def __init__(self):
        self.apiKey= Configuracion.API_KEY
        self.secretKey = Configuracion.SECRET_KEY
        self.url = "http://fapi.binance.com"

    
    #def ObtenerFechaServer (self)-> int: 
    #   return round((datetime.now().timestamp()*1000 ),0)


    def ObtenerFechaServer (self)-> int:
        endPoint = self.url + "/fapi/v1/time"
        r = requests.get(endPoint)
        resp = r.json()
        f=open("TimeNuevo.txt", "a")
        f.write("Time ServerTime = " + str(resp["serverTime"]) + "\n")
        f.write("Time TimeSatamp = " + str(int(round((datetime.now().timestamp()*1000 ),0))) + "\n")
        f.close()
        #return resp["serverTime"]
        return int(round((datetime.now().timestamp()*1000 ),0))

        



    def Firmar(self, parametros:str) -> str:
        m = hmac.new (self.secretKey.encode('utf-8'), parametros.encode('utf-8'), hashlib.sha256)
        return parametros + "&signature=" + m.hexdigest()


    def Encabezados(self, apiKey="") -> dict:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        if apiKey != "":
            headers["X-MBX-APIKEY"] = apiKey
        return headers

    def Log(self, texto:str):
        f = open("Ordenes.log", "a")
        f.write (datetime.now().strftime ("%Y-%m-%d %H:%M:%S") + " -> " + texto + "\n")
        f.close()


    