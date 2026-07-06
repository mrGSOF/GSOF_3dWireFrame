import pygame, math
from Lib3D.Object_WireFrame import Object_wireFrame as Object
from Lib3D.Assembly import Assembly
from Lib3D import WireFrame_display as DISP

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE  = (255,255,255)
YELLOW = (240,240,150)
BLACK  = (0,0,0)
PI = math.pi
        
def clearScreen(screen, color=(255,255,255)) -> None:
  screen.fill(color)
    
def newScreen(title="New", resX=SCREEN_WIDTH, resY=SCREEN_HEIGHT, color=WHITE):
    screenSize = (resX, resY)
    screen = pygame.display.set_mode( screenSize )
    clearScreen(screen, color)
    pygame.display.set_caption(title)
    return screen
    
if __name__ == "__main__":
    import json
    d = 30
    solidHouse = Object(filename="./objects/house.json", color=(0,180,180), name="House").scale(10.0).setOrigin()
    window = Object(filename="./objects/frame.json", color=(200,0,0), name="Window").setCenter(scale=0.8)
    flexHouse = Assembly(objects = (
        Object(filename="./objects/cube.json", color=(190,190,190), name="Body").translate(0,0,0).setOrigin(),
        Object(filename="./objects/pyramid.json", color=(90,90,90), name="Roof").translate(0,-2.5,0).setOrigin(),
        Assembly(objects=(window,), name="Window-Assy").translate(0,0,-1).setOrigin(),
        ),
        connections=[
          [[0,4],[1,0]], #< Point-4 of object-0 to point-0 of object-1
          [[0,5],[1,1]], #< Point-5 of object-0 to point-1 of object-1
          [[0,6],[1,2]], #< Point-6 of object-0 to point-2 of object-1
          [[0,7],[1,3]]  #< Point-7 of object-0 to point-3 of object-1
          ],
          name="Flex-House"
          ).scale(10).rotate(PI,0,0).setOrigin()

    world = Assembly(objects = (
        solidHouse.translate(0,0,0).setOrigin(),
        flexHouse.translate(0,0,d).setOrigin(),
        ))
    pygame.init()
    clock = pygame.time.Clock()
    screen = newScreen("3D Wire Frame Shapes", SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
    wireframe = DISP.WireFrame(screen, pygame.draw.line, scale=50*80, minViewDistance=10)
    fps = 30
    dt = 1/fps
    t = 0.0
    camAngX_r = 0.0
    camAngY_r = 0.0
    roofAng_r = 0.0
    houseAng_r = 0.0
    useMouse = True

    run = True
    while run:
        ### Get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False

        ### Calculate next step state
        camAngX_r += 0.5*dt
        camAngY_r += 1*dt
        roofAng_r = (PI/4/2)*math.sin(2*PI*1*t)
        houseAng_r = (PI/4)*math.sin(2*PI*1.5*t)
        t += dt

        ### Update 3D world
        world.reset()
        solidHouse.rotate(x=0,y=roofAng_r,z=houseAng_r)
        roof = flexHouse.objects[1]
        roof.rotate(x=0,y=roofAng_r,z=0)
        window.rotate(x=0,y=0,z=10*t)
        world.rotate(x=camAngX_r,y=camAngY_r,z=0)
        world.translate(x=0,y=0,z=-600)

        ### Draw 3D world
        clearScreen(screen, YELLOW)
        wireframe.draw(world)
        
        ### Wait for next step time
        if useMouse:
            (mPosX, mPosY) = pygame.mouse.get_pos()
            camAngY_r = 0.01*(mPosX -SCREEN_WIDTH/2)
            camAngX_r = 0.01*(mPosY -SCREEN_HEIGHT/2)
        else:
            camAngX_r += 0.5*dt
            camAngY_r += 1*dt
        clock.tick(30)
        
        ### Display output
        pygame.display.flip()
        
    pygame.quit()
