
from Binance import Binance
from datetime import datetime
import requests

class FuturosConsultas(Binance):
    def __init__(self):
        Binance.__init__(self)

    def ObtenerOperaciones(self, simbolo:str, limite:int=500):
        endPoint = self.url + "/fapi/v1/trades"
        parametro = "symbol=" + simbolo.upper()                     ##upper es volver algo en mayusculas
        if limite != 500 and limite <= 1000 and limite > 0:
            parametro += "&limit=" + str(limite)
        r = requests.get(endPoint, parametro)
        return r.json()


    def ObtenerBalance(self):
        endPoint = self.url + "/fapi/v2/balance"
        parametros = "timestamp=" + str(self.ObtenerFechaServer())
        parametros = self.Firmar(parametros)
        h = self.Encabezados(self.apiKey)
        r = requests.get(endPoint, params=parametros, headers=h)
        return r.json()


    def ObtenerCuentaGeneral (self) ->dict:
        endPoint = self.url + "/fapi/v2/account"
        parametros = "timestamp=" + str(self.ObtenerFechaServer())
        parametros = self.Firmar(parametros)
        h = self.Encabezados(self.apiKey)
        r = requests.get(endPoint, params=parametros, headers=h)
        return r.json()

    def ObtenerPosiciones(self) ->dict:
        ac = self.ObtenerCuentaGeneral()
        if "positions" in ac.keys():
            return ac["positions"]
        return None
    
    def ObtenerPosicion(self, simbolo:str) ->dict:
        pos = self.ObtenerPosiciones()
        ticker = simbolo.upper()
        for item in pos:
            if item["symbol"] == ticker:
                return float(item["positionAmt"])
        return 0.0
