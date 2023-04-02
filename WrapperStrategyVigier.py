# -*- coding: utf-8 -*-

import rsa
from abc import ABC, abstractmethod

class BancoUtilidades(ABC):
    def __init__(self, dueñoDNI):
        self.dueñoUtility = dueñoDNI #Composicion Has a
        self.logDeTransaccion = []
        self.saldo = 0.0
        
    def setDueño(self, dueñoNew):
        self.dueñoUtility = dueñoNew
    
    def getDueño(self):
        return self.dueñoUtility
    
    def setSaldo(self, saldo):
        self.saldo = saldo
    
    def getSaldo(self):
        return self.saldo
        
    def añadirMovimiento(self, mov):
        self.logDeTransaccion.append(mov)
    
    def flushMovimientos(self):
        self.logDeTransaccion = []
    
    def getMovimiento(self):
        return self.logDeTransaccion
    @abstractmethod
    def depositarDinero(self, depositanteDNI, monto):
        pass
    @abstractmethod
    def extraerDinero(self, depositanteDNI, monto):
        pass


class  CajaAhorro(BancoUtilidades):
    def __str__(self):
        s = "Caja de Ahorro del Cliente %d, con Saldo %r" %(self.getDueño(), self.getSaldo()) + "\n"
        movStr = '\n'.join(map(str, self.getMovimiento()))
        s = s + "El Log de movimientos es: \n"+ movStr + "\n"
        return s
    def depositarDinero(self, depositanteDNI, monto) :
        if depositanteDNI == self.dueñoUtility :
            self.setSaldo(monto + self.getSaldo())
            self.añadirMovimiento("Deposito de " + str(self.getDueño()) + " Monto: " + str(monto))
    def extraerDinero(self, depositanteDNI, monto) :
        if depositanteDNI == self.dueñoUtility and 0.0 <= self.getSaldo() - monto :
            self.setSaldo(self.getSaldo() - monto)
            self.añadirMovimiento("Extraccion de " + str(self.getDueño()) + " Monto: " + str(monto))
        
    

class CajaAhorroDecorador(BancoUtilidades):
    def __init__(self, dueñoDNI, cajaAhorroObj):
        self.CAObj = cajaAhorroObj
    def __str__(self):
        return (self.CAObj.__str__())
    #Todo observador que usen los wrapper tambien tienen que ir para dentro
    #sino puede pasar que al componer wrapper los observadores que se usen en la
    #logica se pierdan
    def getSaldo(self):
        return self.CAObj.getSaldo()
    
#Se puede ver que son wrappers de la composicion de objetos
class CajaAhorroResolucion1(CajaAhorroDecorador):
    #En esta primera Resolucion del Banco Central, todo cliente puede depositar en la caja de otro
    def depositarDinero(self, depositanteDNI, monto) :
        if depositanteDNI != self.CAObj.dueñoUtility :
            self.CAObj.setSaldo(monto + self.CAObj.getSaldo())
            self.CAObj.añadirMovimiento("Deposito de " + str(depositanteDNI) + " Monto: " + str(monto))
        self.CAObj.depositarDinero(depositanteDNI,monto)
            
    def extraerDinero(self, depositanteDNI, monto) :
        self.CAObj.extraerDinero(depositanteDNI,monto)
        
    
    
class CajaAhorroResolucion2(CajaAhorroDecorador):
    #En esta segunda Resolucion del Banco Central, solo voy se van a poder efectuar extracciones que
    #superen el 20% del valor depositado
    def depositarDinero(self, depositanteDNI, monto) :
        self.CAObj.depositarDinero(depositanteDNI,monto)
    def extraerDinero(self, depositanteDNI, monto) :
        if monto < (20.0*self.CAObj.getSaldo())/100.0 :
            self.CAObj.extraerDinero(depositanteDNI,monto)

class CajaFuerte(BancoUtilidades):
    def __init__(self, dueñoDNI, numCjaFuerte, encriptacioObj = None, declaracionJurada = None):
        super().__init__(dueñoDNI) 
        self.numCjaFuerte = numCjaFuerte
        self.encriptacionObj = encriptacioObj
        self.ddjj = declaracionJurada
        #print(self.getDueño())
    def getEncriptacion(self):
        return self.encriptacionObj
    
    def setEncriptacion(self, encriptacionNew):
        self.encriptacionObj = encriptacionNew
        
    def getNumCja(self):
        return self.numCjaFuerte
    
    def setNumCja(self, numCjaNew):
        self.numCjaFuerte = numCjaNew
    
    def setDDJJ(self, txt):
        self.ddjj = txt
    
    def getDDJJ(self, shiftN = 0):
        e, d = self.encriptacionObj.encriptar(self.ddjj, shiftN)
        return e
    
    def depositarDinero(self, depositanteDNI, monto):
        pass
    
    def extraerDinero(self, depositanteDNI, monto):
        pass
        
 #_______________________________________________________________________
class AlgoritmosCifrado(ABC):
     @abstractmethod
     def encriptar(self, txt, shifty = 0):
         pass
     
class RSA (AlgoritmosCifrado):
    def encriptar(self, txt, shifty = 0):
        pubkey, privkey = rsa.newkeys(512)
        enctex = rsa.encrypt(txt.encode(),pubkey)
        dectex = rsa.decrypt(enctex, privkey).decode()
        return enctex, dectex
    
class SimpleCesar(AlgoritmosCifrado):
    def encriptar(self, txt, shifty = 0):
        
        abcUP="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        abcLW="abcdefghijklmnñopqrstuvwxyz" 

        shifteadp = shifty % len(abcUP)
        cifrad=""

        for c in txt:
            if c in abcUP:
                cifrad += abcUP[(abcUP.index(c)+shifteadp)%(len(abcUP))]
            elif c in abcLW:
                    cifrad += abcLW[(abcLW.index(c)+shifteadp)%(len(abcLW))]
            else:
                cifrad+=c

        return cifrad, txt
#________________________________________________________________________
"""
#TEST
#WRAPPER
#CajaDeAhorros sin Restricciones
UtilidadCliente1 = CajaAhorro(123456789)
UtilidadCliente1.depositarDinero(123456789, 100.0)
UtilidadCliente1.extraerDinero(123456789, 100.0)
print(UtilidadCliente1)
UtilidadCliente1.flushMovimientos() #Flusheo el nucleo del wrapper
UtilidadCliente1.setSaldo(0.0)
print("\n")
#CajaDeAhorros Con Resolucion 1
ConR1Cliente1 = CajaAhorroResolucion1(123456789, UtilidadCliente1)
ConR1Cliente1.depositarDinero(123456789, 100.0)
ConR1Cliente1.depositarDinero(987654321, 100.0)
ConR1Cliente1.extraerDinero(123456789, 100.0)
print(ConR1Cliente1)
UtilidadCliente1.flushMovimientos()
UtilidadCliente1.setSaldo(0.0)
print("\n")
#CajaDeAhorro Con Resolucion 2
ConR2Cliente1 = CajaAhorroResolucion2(123456789, UtilidadCliente1)
ConR2Cliente1.depositarDinero(123456789, 100.0)
ConR2Cliente1.depositarDinero(987654321, 100.0)
ConR2Cliente1.extraerDinero(123456789, 10.0)
print(ConR2Cliente1)
UtilidadCliente1.flushMovimientos()
UtilidadCliente1.setSaldo(0.0)
print("\n")
#CajaDeAhorro Con Resolucion 1 y 2
ConR1R2Cliente1 = CajaAhorroResolucion2(123456789, ConR1Cliente1)
ConR1R2Cliente1.depositarDinero(123456789, 100.0)
ConR1R2Cliente1.depositarDinero(987654321, 100.0)
ConR1R2Cliente1.extraerDinero(123456789, 39.9)
print(ConR1R2Cliente1)
UtilidadCliente1.flushMovimientos()
UtilidadCliente1.setSaldo(0.0)
print("\n")


#Encriptacion de Texto Strategy
#RSA
rsaEncode = RSA()
encodeRSA,decodeRSA = rsaEncode.encriptar("HolaMundoCruel")
print("Encode RSA: %s \nDecode RSA: %s \n" %(encodeRSA,decodeRSA))
#Ceasar
ceasarEncode = SimpleCesar()
encodeCesar,decodeCesar = ceasarEncode.encriptar("HolaMundoCruel", 5)
print("Encode CS: %s \nDecode CS: %s \n" %(encodeCesar,decodeCesar))
# STRATEGY, Dinamico en tiempo de ejecucion
CajaFuerteCliente1 = CajaFuerte(123456789,1) #No pongo los keyboard args
CajaFuerteCliente1.setEncriptacion(rsaEncode)
CajaFuerteCliente1.setDDJJ("Hola Soy Franco, Mucho Gusto")
Cliente1Encode = CajaFuerteCliente1.getDDJJ()
print("Con el RSA se encode: %s"  %(Cliente1Encode))
CajaFuerteCliente1.setEncriptacion(ceasarEncode)
Cliente1Encode = CajaFuerteCliente1.getDDJJ(shiftN = 5)
print("Con el Ceasar se encode: %s"  %(Cliente1Encode))
"""