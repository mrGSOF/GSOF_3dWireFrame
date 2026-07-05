def _findLine(x1,y1,x2,y2) -> list:
        DX = x2 -x1
        DY = y2 -y1
        Ay = DY/DX
        By = y2 -Ay*x2
        return (Ay, By)

def calcLine(a, b, x) -> float:
    return a*x +b

class WireFrame():
    def __init__(self, screen, line, f=1, scale=1000.0, maxViewDistance=10000):
        self.screen = screen #< Object to draw on
        self.line = line     #< function to draw a line
        self.f = f           #< Perspective factor
        self.scale = scale   #< Lens zoom
        self.maxViewZ = maxViewDistance #< 
        self.minViewZ = abs(1.0)        #< 
        self.centerX, self.centerY = (int(screen.get_width()/2), int(screen.get_height()/2))
        
    def draw(self, obj, color=None) -> None:
        """  """
        for line in obj.getLines():
            p1, p2 = line.points
            #p1[2], p2[2] = -p1[2], -p2[2]
            z0 = -self.minViewZ
            if (p1[2] < z0) or (p2[2] < z0):
                ### At least one end of the line is infront of the camera
                self.clip(p1,p2)
                p1 = self.camera(p1)
                p2 = self.camera(p2)
                lcolor = line.color if color == None else color
                self.drawLine( lcolor, p1, p2 )

    def clip(self, p1, p2) -> None:
        z0, z1, z2 = -self.minViewZ, p1[2], p2[2]
        x1, x2 = p1[0], p2[0]
        y1, y2 = p1[1], p2[1]
        if z1 != z2:
            Ax, Bx = _findLine(z1,x1,z2,x2)
            Ay, By = _findLine(z1,y1,z2,y2)
            if z1 > z0:
                p1[0], p1[1], p1[2] = calcLine(Ax, Bx, z0), calcLine(Ay, By, z0), z0
            elif z2 > z0:
                p2[0], p2[1], p2[2] = calcLine(Ax, Bx, z0), calcLine(Ay, By, z0), z0

    def camera(self, point) -> list:
        """ Perspective projection <https://en.wikipedia.org/wiki/3D_projection> """
        x, y, z = point
        s =self.scale/10
        z *= -1
        if (self.f != 0):
            s = self.scale/z
        return (x*s, y*s, z)

    def drawLine(self, color, p0, p1):
        """  """
        p0 = (self.centerX +p0[0], self.centerY -p0[1])
        p1 = (self.centerX +p1[0], self.centerY -p1[1])
        self.line( self.screen, color, p0, p1 ) #< Line from P0 to P1
