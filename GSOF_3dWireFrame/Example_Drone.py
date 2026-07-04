#!/usr/bin/python
"""
 * Example_F16.py
 * Created on: 31 May 2026
 * Improved for: 31 May 2026
 * Author: Tzur Soffer
 * Copyright (C) 2026 Tzur Soffer
"""

try:
    import pymeshlab
except:
    raise ValueError("could not find pymeshlab. Run ```pip install pymeshlab```")

import pygame, math
from MathLib import MathLib
from Lib3D.Object_WireFrame import Object_wireFrame
from Lib3D.Assembly import Assembly
from Lib3D import Objects
from Lib3D import WireFrame_display as DISP
from Lib3D.Utils import Colors
from Drone_Class import View

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PI = math.pi

def drawWireFrame(screen, obj, color=None) -> None:
    for line in obj.getLines():
        x0, y0, z0 = line.p0
        x1, y1, z1 = line.p1
        lcolor = color
        if lcolor == None:
            lcolor = line.color
        pygame.draw.line( screen, lcolor, (x0, y0), (x1, y1) ) #< Line from P0 to P1

def clearScreen(screen, color=(255,255,255)) -> None:
  screen.fill(color)
    
def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=Colors.WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen

def rotatePR(p, r, yaw):
    R = MathLib.DCM_V2(yaw)
    return MathLib.MxV_2x2(R, [p, r])

def quadMix(p, r):
    M = [
        [ 1, -1],  # A
        [ 1,  1],  # B
        [-1,  1],  # C
        [-1, -1],  # D
    ]
    return MathLib.MxV(M, [p, r])

def computePropellers(maxRps, p, r, yaw):
    p2, r2 = rotatePR(p, r, yaw)

    props = quadMix(p2, r2)  # mix WITHOUT maxRps first

    # Normalize
    maxVal = 0
    for v in props:
        if abs(v) > maxVal:
            maxVal = abs(v)

    # Scale if needed
    if maxVal > 1.0:
        props = MathLib.scaleV(props, 1.0 / maxVal)

    # Apply maxRps
    props = MathLib.scaleV(props, maxRps)

    A = MathLib.clip(props[0], -maxRps, maxRps)
    B = MathLib.clip(props[1], -maxRps, maxRps)
    C = MathLib.clip(props[2], -maxRps, maxRps)
    D = MathLib.clip(props[3], -maxRps, maxRps)

    return A, B, C, D

def sign(val):
    if val >= 0:
        return 1
    return -1


if __name__ == "__main__":
    pygame.init()
    ground = Object_wireFrame(
       obj=Objects.net(25,25), color=(0,100,0))\
       .scale(0.2)\
       .rotate(x=math.pi/2, y=0, z=0)\
       .translate(-250, -200, -250)\
       .setOrigin()

    drone = View()\
          .scale(1.0)\
          .translate(100, 100, -100).setOrigin()

    world = Assembly(objects=(ground, drone)).translate(0,0,-1000).setOrigin()

    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, Colors.WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=20.0)

    fps = 30
    maxRps = 2
    dt = 1/fps
    t = 0
    useMouse = True
    mPosZ = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False
        world.reset()
        clearScreen(screen)

        keys = pygame.key.get_pressed()

        if useMouse:
            (mPosX, mPosY) = pygame.mouse.get_pos()
            mPosZ += (keys[pygame.K_z] -keys[pygame.K_x])*2
            x = mPosX/SCREEN_WIDTH -0.5
            y = mPosY/SCREEN_HEIGHT -0.5
            z = mPosZ/360
        else:
            x += 0.5*dt
            y += 1*dt
            z = 0
        camAngX_r = y*PI
        camAngY_r = z*PI
        camAngZ_r = x*PI
        
        print(computePropellers(maxRps, camAngX_r, camAngY_r, camAngZ_r))
        A, B, C, D = computePropellers(maxRps/2, camAngX_r, camAngY_r, camAngZ_r)
        A+=maxRps/2*sign(A)
        B+=maxRps/2*sign(B)
        C+=maxRps/2*sign(C)
        D+=maxRps/2*sign(D)
        drone.setPropellors(A, B, C, D)
        drone.rotate(-camAngX_r,-camAngY_r,-camAngZ_r, centerAt=(100, 100, -100))
        drone.tick(dt)
        wireframe.draw(world)

        t += dt
        clock.tick(30)

        pygame.display.flip()

    pygame.quit()
