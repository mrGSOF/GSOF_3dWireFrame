#!/usr/bin/python
"""
 * F16_Class.py
 * Created on: 6 Jan 2025
 * Improved for: 25 May 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

import copy
from math import pi
try:
   from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
   from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
   from GSOF_3dWireFrame.Lib3D.Utils import Colors
except:
   print("GSOF_Wireframe3D module isn't installed")

degToRad = pi/180

class View(Assembly):
    """Constructs the gauges screen"""
    def __init__(self, folder='./'):
        self.time = 0.0
        axis  = Object(
            filename="%s/objects/axis.json"%folder, color=Colors.GREEN)\
            .scale(50.0)\
            .translate(0, 0, 150)\
            .setOrigin()

        self.drone = Object(
            filename="%s/objects/Drone/Body.stl"%folder, color=Colors.BLUE)\
            .setCenter(scale=1.0, method="arithCenter")

        propellorObj = Object(filename="%s/objects/Drone/Blade.stl"%folder, color=Colors.RED)\
            .translate(0,20,0)\
            .setCenter(scale=1.0, method="arithCenter")\
            .setOrigin()
   
        self.propellorA = copy.deepcopy(propellorObj)
        self.propellorB = copy.deepcopy(propellorObj)
        self.propellorC = copy.deepcopy(propellorObj)
        self.propellorD = copy.deepcopy(propellorObj)

        self.propellorA.color = Colors.RED
        self.propellorB.color = Colors.BLACK
        self.propellorC.color = Colors.GRAY
        self.propellorD.color = Colors.YELLOW

        super().__init__(objects=(axis, self.drone,
                                  Assembly(objects=(self.propellorA,)).translate(-95,0,-90).setOrigin(),
                                  Assembly(objects=(self.propellorB,)).translate(100,0,-90).setOrigin(),
                                  Assembly(objects=(self.propellorC,)).translate(90,0,100).setOrigin(),
                                  Assembly(objects=(self.propellorD,)).translate(-85,0,100).setOrigin()
                                  ))

    def setPropellorRps(self, propellor, rps) -> None:
        propellor.rotate(x=0, y=rps*self.time*6.28, z=0)

    def setPropellors(self, A, B, C, D) -> None:
        self.setPropellorRps(self.propellorA, A)
        self.setPropellorRps(self.propellorB, B)
        self.setPropellorRps(self.propellorC, C)
        self.setPropellorRps(self.propellorD, D)
    
    def tick(self, dt):
        self.time+=dt
