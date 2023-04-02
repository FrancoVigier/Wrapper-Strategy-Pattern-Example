# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 19:47:29 2023

@author: usuario
"""

import unittest
import WrapperStrategyVigier as ws
from parameterized import parameterized
#import socket
#import utils


class TestUtils(unittest.TestCase):
    @parameterized.expand([
        [100.0, 123456789, 987654321]
    ])
    def test_depositarextraerDinero(self, monto, dni, dniAjeno):
        UtilidadCliente1 = ws.CajaAhorro(dni)
        
        UtilidadCliente1.depositarDinero(dni, monto)
        self.assertTrue(UtilidadCliente1.getSaldo() == monto)
        
        UtilidadCliente1.depositarDinero(dniAjeno, monto)
        self.assertTrue(UtilidadCliente1.getSaldo() == monto)
        
        UtilidadCliente1.extraerDinero(dni, monto*2)
        self.assertTrue(UtilidadCliente1.getSaldo() == monto)
        
        UtilidadCliente1.extraerDinero(dniAjeno, monto)
        self.assertTrue(UtilidadCliente1.getSaldo() == monto)
        
        UtilidadCliente1.extraerDinero(dni, monto)
        self.assertTrue(UtilidadCliente1.getSaldo() == 0.0)
        
    @parameterized.expand([
        [123456789, 987654321, 1000.0, 500.0]
    ])
    def test_depositarextraerDineroR1(self, dniDueño, dniAjeno, deposito, extraccion):
        UtilidadCliente1 = ws.CajaAhorro(dniDueño)
        ConR1Cliente1 = ws.CajaAhorroResolucion1(dniDueño, UtilidadCliente1)
        
        ConR1Cliente1.depositarDinero(dniDueño, deposito)
        self.assertTrue(UtilidadCliente1.getSaldo() == deposito)
        
        ConR1Cliente1.depositarDinero(dniAjeno, deposito)
        self.assertTrue(UtilidadCliente1.getSaldo() == 2*deposito)
        
        ConR1Cliente1.extraerDinero(dniDueño, extraccion)
        self.assertTrue(UtilidadCliente1.getSaldo() == 2*deposito - extraccion )
        
        ConR1Cliente1.extraerDinero(dniAjeno, extraccion)
        self.assertTrue(UtilidadCliente1.getSaldo() == 2*deposito - extraccion )

    @parameterized.expand([
        [123456789, 987654321, 1000.0, 500.0, 125.0]
    ])
    def test_depositarextraerDineroR2(self, dniDueño, dniAjeno, deposito, extraccionInvalida, extraccionValida):
        UtilidadCliente1 = ws.CajaAhorro(dniDueño)
        ConR2Cliente1 = ws.CajaAhorroResolucion2(dniDueño, UtilidadCliente1)
        
        ConR2Cliente1.depositarDinero(dniDueño, deposito)
        self.assertTrue(UtilidadCliente1.getSaldo() == deposito)
        
        ConR2Cliente1.depositarDinero(dniAjeno, deposito)
        self.assertTrue(UtilidadCliente1.getSaldo() == deposito)
        
        ConR2Cliente1.extraerDinero(dniAjeno, extraccionInvalida)
        self.assertTrue(UtilidadCliente1.getSaldo() == deposito )
        
        ConR2Cliente1.extraerDinero(dniDueño, extraccionInvalida)
        self.assertTrue(UtilidadCliente1.getSaldo() == deposito )
        
        ConR2Cliente1.extraerDinero(dniDueño, extraccionValida)
        self.assertTrue(UtilidadCliente1.getSaldo() == deposito - extraccionValida )
   
    @parameterized.expand([
        [123456789, 987654321, 1000.0, 500.0, 125.0]
    ])
    def test_depositarextraerDineroR1R2(self, dniDueño, dniAjeno, deposito, extraccionInvalida, extraccionValida):
        UtilidadCliente1 = ws.CajaAhorro(dniDueño)
        ConR1Cliente1 = ws.CajaAhorroResolucion1(dniDueño, UtilidadCliente1)
        ConR1R2Cliente1 = ws.CajaAhorroResolucion2(dniDueño, ConR1Cliente1)
    
    
        ConR1R2Cliente1.depositarDinero(dniDueño, deposito)
        self.assertTrue(UtilidadCliente1.getSaldo() == deposito)
    
        ConR1R2Cliente1.depositarDinero(dniAjeno, deposito)
        self.assertTrue(UtilidadCliente1.getSaldo() == 2*deposito)
    
        ConR1R2Cliente1.extraerDinero(dniAjeno, extraccionInvalida)
        self.assertTrue(UtilidadCliente1.getSaldo() == 2*deposito )
    
        ConR1R2Cliente1.extraerDinero(dniDueño, extraccionValida)
        self.assertTrue(UtilidadCliente1.getSaldo() == 2*deposito - extraccionValida )


if __name__ == '__main__':
    unittest.main()