#!/usr/bin/python
"""
 * F16_Class.py
 * Created on: 6 Jan 2025
 * Improved for: 25 May 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
try:
   from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
   from GSOF_3dWireFrame.Lib3D.Object_base import Object_base
   from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
   from GSOF_3dWireFrame.Lib3D import Objects
   _3D_active = True
except:
   _3D_active = False
   print("GSOF_Wireframe3D module isn't installed")

degToRad = pi/180
#YELLOW = (255,255,140)
YELLOW = (125,125,0)
BLACK  = (0,0,0)
RED    = (255,0,0)
GREEN  = (0,170,0)
BLUE   = (0,0,255)
GRAY   = (50,50,50)

class State():
    def __init__(self,
                 azimuth_d=0,
                 pitch_d=0,
                 roll_d=0,
                 thrust_lbf=0,
                 wowNose_b=False,
                 wowLeft_b=False,
                 wowRight_b=False):
        self.azimuth_d = azimuth_d
        self.pitch_d   = pitch_d
        self.roll_d    = roll_d
        self.thrust_lbf = thrust_lbf
        self.wowNose_b  = wowNose_b
        self.wowLeft_b  = wowLeft_b
        self.wowRight_b = wowRight_b

class Commands():
    def __init__(self,
                 leftAliron_d=0, rightAliron_d=0,
                 leftElevator_d=0, rightElevator_d=0,
                 rudder_d=0, speedbrake_d=0,
                 throttle=0,
                 gearsDown_b=True):
        self.leftAliron_d    = leftAliron_d
        self.rightAliron_d   = rightAliron_d
        self.leftElevator_d  = leftElevator_d
        self.rightElevator_d = rightElevator_d
        self.rudder_d        = rudder_d
        self.speedbrake_d    = speedbrake_d
        self.gearsDown_b     = gearsDown_b

class F16_View(Assembly):
    """Constructs the gauges screen"""
    def __init__(self, folder='./'):
        self.time = 0.0
        axis  = Object(
           filename="%s/objects/axis.json"%folder, color=GREEN)\
           .scale(50.0)\
           .translate(0, 0, 150)\
           .setOrigin()

        self.plane = Object(
            filename="%s/objects/f16.stl"%folder, color=BLUE, name="F16")\
            .setCenter(scale=1.0, method="arithCenter")
        
        self.plume = Object(
           filename="%s/objects/Plume.json"%folder, color=RED)\
           .setCenter(scale=30, rotate=(180*degToRad, 0, 0))
        plume = Assembly(objects=(self.plume,))   
        plume.translate(0, 0, -90).setOrigin()
        
        self.nw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="NW")
        self.nwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW, name="NWOW")
        nw = Assembly(objects=(self.nw, self.nwow), name="NW-Assy")\
           .translate(0, -2, 0).scale(8).translate(0, -30, 80).setOrigin()           

        self.lw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="LW")
        self.lwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW)
        lw = Assembly(objects=(self.lw, self.lwow), name="LW-Assy")\
           .translate(0, -2, 0).rotate(x=0, y=0, z=degToRad*15)\
           .scale(8).translate(18, -30, 0).setOrigin()           

        self.rw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="RW")
        self.rwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW)
        rw = Assembly(objects=(self.rw, self.rwow), name="RW-Assy")\
           .translate(0, -2, 0).rotate(x=0, y=0, z=-degToRad*15)\
           .scale(8).translate(-18, -30, 0).setOrigin()           

        self.gears = Assembly(objects=(nw,
                                       rw,
                                       lw
                                       ))
        super().__init__(objects=(axis, self.plane, plume, self.gears))

    def setControls(self, time, commands=None, state=None):
        """Update all elements"""
        self.time += 0.1

        if state != None:
            self.setWOW(state.wowNose_b, state.wowLeft_b, state.wowRight_b)
            self.setExahustPlume(state.thrust_lbf)
            heading =  state.azimuth_d*degToRad
            pitch   = -state.pitch_d*degToRad
            roll    =  state.roll_d*degToRad
            self.setAttitude(heading, pitch, roll)

        if commands != None:
            self.setFCS(commands.leftAliron_d,
                        commands.rightAliron_d,
                        commands.leftElevator_d,
                        commands.rightElevator_d,
                        commands.rudder_d,
                        commands.speedbrake_d)
            self.setGearsDown(commands.gearsDown_b)

    def setAttitude(self, heading, pitch, roll) -> None:
        self.rotate( y=-heading, x=-pitch, z=-roll )

    def setExahustPlume(self, thrust_lbf) -> None:
        thrustMAX = 6360
        plume = thrust_lbf/thrustMAX
        if plume > 1:
            plume = 1
        elif plume < 0:
            plume = 0
        plumeColor = (255, 255*(1-plume), 255*(1-plume))
        self.plume.rotate(x=0, y=0, z=self.time*plume)
        self.plume.scale(plume).color = plumeColor
       
    def setFCS(self, lAliron_deg, rAliron_deg, lElevator, rElevator, rudder_deg, sb_deg) -> None:
        return
      
    def setGearsDown(self, downCmd) -> None:
        if downCmd == False:
           self.gears.scale(0.0)
        else:
           self.gears.scale(1.0)

    def setWOW(self, nose, left, right) -> None:
        time = int(self.time*10)
        blink = bool(time&0b010)
        self.nwow.rotate(x=0, y=0, z=4*self.time)\
                 .scale(int(nose and blink))
        self.lwow.rotate(x=0, y=0, z=4*self.time)\
                 .scale(int(left and blink))
        self.rwow.rotate(x=0, y=0, z=4*self.time)\
                 .scale(int(right and blink))
