from FuturosConsultas import FuturosConsultas as Consultas
from FuturosOrdenes import FuturosOrdenes as Ordenes
from Binance import Binance
import json
import Configuracion

class FuturosBot (Binance):
    orden = ""
    ticker = ""
    entrada = ""

    def __init__(self):
        Binance.__init__(self)

    
    def ObtenerComando (self, texto:str)-> str:
        compra = ["comprar", "compra", "buy", "long", "largo" ]
        venta  = ["vender", "venta", "sell", "short", "corto" ]
        cerrar = ["cerrar", "cierra", "cierre", "close" ]
        if texto.lower() in compra:
            return "Comprar"      
        if texto.lower() in venta:
            return "Vender"
        if texto.lower() in cerrar:
            return "Cerrar"

    def ObtenerTicker(self, texto:str) ->str:
        ticker = texto.upper()
        if "PERP" in ticker:
            ticker = ticker.replace ("PERP","")
        if "USDT" not in ticker:
            ticker += "USDT"
        return ticker

    def Desglozar(self, mensaje:str):
        x = mensaje.split()
        self.orden = self.ObtenerComando (x[0])
        self.ticker = self.ObtenerTicker (x[1])
    
    def ObtenerPosicion(self, ticker:str)->float:
        c = Consultas()
        return c.ObtenerPosicion(ticker)

    def ObtenerCantidad (self, ticker:str) -> float:
        f = open ("Cantidades.json", "r")
        cantidades = json.load(f)
        f.close()
        if ticker in cantidades:
            return cantidades [ticker]
        return 0.0

    
         





    def Entrar(self, mensaje:str)-> bool:

        #desglozar mensaje
        self.Desglozar (mensaje)

        #obtener la posicion actual del ticker
        pos = 0
        pos = self.ObtenerPosicion(self.ticker) 

        #obtener la cantidad a operar segun el ticker
        cantidad = self.ObtenerCantidad (self.ticker)


        print(self.orden + "->" + self.ticker + " " + str(cantidad) + "   Pos actual:" + str(pos))

        o = Ordenes()
        if self.orden == "Comprar":
            if pos < 0:
                o.CerrarVentaMarket (self.ticker, abs(pos))
                self.Log("Cerrando venta previa "+ self.ticker + " Cant:" + str(abs(pos)))
                pos = 0
            maximo = cantidad * Configuracion.Maximo_operaciones
            if abs(pos) + cantidad > maximo:
                self.Log (self.orden + ":" + self.ticker + " Cant:" + str(cantidad) + " -> Supera Maxima Cantidad de Operaciones")
                return
            o.ComprarMarket(self.ticker, cantidad)
            self.Log (self.orden + ":" + self.ticker + " Cant:" + str(cantidad))
            
        
        if self.orden == "Vender":
            if pos > 0:
                o.CerrarCompraMarket (self.ticker, pos)
                self.Log("Cerrando Compra previa "+ self.ticker + " Cant:" + str(pos))
                pos = 0
            maximo = cantidad * Configuracion.Maximo_operaciones
            if abs(pos) + cantidad > maximo:    
                self.Log (self.orden + ":" + self.ticker + " Cant:" + str(cantidad) + " -> Supera Maxima Cantidad de Operaciones")
                return
            o.VenderMarket(self.ticker, cantidad)
            self.Log (self.orden + ":" + self.ticker + " Cant:" + str(cantidad))
        
        if self.orden == "Cerrar":
            if pos > 0:
                o.CerrarCompraMarket (self.ticker, pos)
                self.Log("Cerrando Compra previa "+ self.ticker )
            if pos < 0:
                o.CerrarVentaMarket (self.ticker, abs(pos))
                self.Log("Cerrando Venta previa "+ self.ticker )
            
    
                
                