import pygame, math
from Lib3D.Object_WireFrame import Object_wireFrame as Object
from Lib3D.Object_base import Object_base
from Lib3D.Assembly import Assembly
from Lib3D import WireFrame_display as DISP
from Lib3D import Objects

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
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
    ### 1. Build the ground
    net    = Object(obj=Objects.net(25,20), color=(0,100,0), name="NET")\
             .setCenter(pos=(0,0,0), rotate=(PI/2, 0, 0), scale=0.2 )
    axis1 = Object(filename="./objects/axis.json", color=(10,10,10), name="WorldAxis" )\
       .scale(100.0)\
       .setOrigin()
    ground = Assembly(objects=(net, axis1), name="Ground").translate(-200, 0, 0).setOrigin()    

    ### 2. Build the sun
    sun = Object(obj=Objects.sphere(500, 15, color=(225,220,50)), name="SUN")
    sun.setCenter(scale=0.15, rotate=(PI/2,0,0))
    sun.translate(0, 250, 300)  #< More up (Y) and forward (Z) to the center of the net 
    sun.setOrigin()

    ### 3. Build the plane
    axis2  = Object(
       filename="./objects/axis.json", color=(10,10,10 ))\
       .scale(100.0)\
       .setOrigin()
    f16  = Object(filename="./objects/F16.stl", color=(0,0,255), name="F16")\
              .setCenter(scale=1.0, rotate=(0,-PI/2,0), method="arithCenter")
    plane  = Assembly(objects=[f16, axis2], name="Plane")\
             .rotate(0.5*-3.14/2,0,0)\
             .translate(0,250,0)\
             .setOrigin()

    ### 4. Build the world
    world  = Assembly(objects = (
        ground,
        plane,
        sun,
        ), name="World")

    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, f=1, scale=500.0)

    fps = 30
    dt = 1/fps
    t = 0.0
    camAngX_r = 0.0
    camAngY_r = 0.0
    f16Ang_r  = 0.0
    useMouse = True
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        world.reset()
        #world.rotate(x=1.8,y=3.14,z=0.3)
        world.rotate(x=camAngX_r,y=camAngY_r,z=0)
        #world.rotate(x=camAngX_r,y=camAngY_r,z=0)
        f16.rotate(0, f16Ang_r, 0)
        world.translate(x=0,y=0,z=-1000)

        ### Draw 3D world
        clearScreen(screen, WHITE)
        wireframe.draw(world)
        
        ### Wait for next step time
        if useMouse:
            (mPosX, mPosY) = pygame.mouse.get_pos()
            camAngY_r = 0.01*(mPosX -SCREEN_WIDTH/2)
            camAngX_r = 0.01*(mPosY -SCREEN_HEIGHT/2)
        else:
            camAngX_r += 0.5*dt
            camAngY_r += 1*dt
        f16Ang_r += 4*dt
        t += dt
        clock.tick(30)
        
        ### Display output
        pygame.display.flip()

    pygame.quit()
