#!/usr/bin/python
"""
 * Example_F16.py
 * Created on: 31 May 2026
 * Improved for: 31 May 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

try:
    import pymeshlab
except:
    raise ValueError("could not find pymeshlab. Run ```pip install pymeshlab```")

import pygame, math
from Lib3D.Object_WireFrame import Object_wireFrame
from Lib3D.Assembly import Assembly
from Lib3D import Objects
from Lib3D import WireFrame_display as DISP
from F16_Class import F16_View, Commands, State 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLUE = (220,220,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
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
    
def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen

if __name__ == "__main__":
    import copy
    ground = Object_wireFrame(
       obj=Objects.net(25,25), color=(0,100,0))\
       .scale(0.2)\
       .rotate(x=math.pi/2, y=0, z=0)\
       .translate(-250, -200, -250)\
       .setOrigin()

    f16 = F16_View()\
          .scale(1.0)\
          .translate(100, 100, -100).setOrigin()
    f16.plane.color = BLACK

    rotateBy = (0*3.14/4, 1*3.14/8, 0)
    f16_1 = copy.deepcopy(f16)
    f16_1.rotate(*rotateBy, centerAt=(100,100,-100))\
         .setOrigin()
    f16_1.plane.color = RED

    rotateBy = (0*3.14/4, -1*3.14/8, 0)
    f16_2 = copy.deepcopy(f16)
    f16_2.translate(-100, -100, 100)\
          .rotate(*rotateBy)\
          .translate(100, 100, -100)\
          .translate(-100, 0, 100)\
          .setOrigin()
    f16_2.plane.color = GREEN

    world = Assembly(objects=(ground, f16, f16_1, f16_2))

    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=50, scale=20.0)

    fps = 30
    dt = 1/fps
    t = 0.0
    camAngX_r = 0.0
    camAngY_r = 0.0
    camAngZ_r = 0.0
    commands  = Commands()
    mPosZ = 0.0
    state = State(thrust_lbf=6000)
    useMouse = True

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False
        ### Wait for next step time
        keys = pygame.key.get_pressed()
        state.thrust_lbf  += (keys[pygame.K_q] -keys[pygame.K_a])*200
        commands.gearsDown_b += keys[pygame.K_b] -keys[pygame.K_g]
        commands.gearsDown_b = min(1, max(0,commands.gearsDown_b))
        state.wowNose_b  = bool(keys[pygame.K_2])
        state.wowLeft_b  = bool(keys[pygame.K_1])
        state.wowRight_b = bool(keys[pygame.K_3])
        print(state.wowLeft_b, state.wowNose_b, state.wowRight_b)

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
        commands.rudder_d = z*30
        commands.leftAliron_d   = -25*x
        commands.rightAliron_d  = 25*x
        commands.leftElevator = 0.5*commands.leftAliron_d +25*y
        commands.rightElevator = 0.5*commands.rightAliron_d  +25*y
        camAngX_r = y*PI
        camAngY_r = z*PI
        camAngZ_r = x*PI

        world.reset()
        f16.setControls(t, commands, state)
        world.transform(rotate=(camAngX_r,camAngY_r,camAngZ_r), translate=(0,0,-1000))
        #world.transform(rotate=(3.14/2, 0.0*3.14, 0), translate=(0,0,-1000))

        ### Draw 3D world
        clearScreen(screen, BLUE)
        wireframe.draw(world)
        
        t += dt
        clock.tick(30)
        
        ### Display output
        pygame.display.flip()

    pygame.quit()
