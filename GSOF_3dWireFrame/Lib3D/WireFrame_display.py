def _findLine(x1,y1,x2,y2) -> list:
        DX = x2 -x1
        DY = y2 -y1
        Ay = DY/DX
        By = y2 -Ay*x2
        return (Ay, By)

def calcLine(a, b, x) -> float:
    return a*x +b

class WireFrame():
    def __init__(self, screen, line, f=1, scale=1000.0, minViewDistance=1, maxViewDistance=10000):
        self.screen = screen #< Object to draw on
        self.line = line     #< function to draw a line
        self.f = f           #< Perspective factor
        self.scale = scale   #< Lens zoom
        print("ViewDistance between %1.2f to %1.2f"%(minViewDistance,maxViewDistance))
        self.minViewZ = abs(minViewDistance) #< 
        self.maxViewZ = abs(maxViewDistance) #< 
        self.centerX, self.centerY = (int(screen.get_width()/2), int(screen.get_height()/2))
        
    def draw(self, obj, color=None) -> None:
        """  """
        for line in obj.getLines():
            p1, p2 = line.points
            #p1[2], p2[2] = -p1[2], -p2[2]
            zmin, zmax = -self.minViewZ, -self.maxViewZ
            if (p1[2] > zmax) or (p2[2] > zmax):
                ### Both end are in view distance
                if (p1[2] < zmin) or (p2[2] < zmin):
                    ### At least one end of the line is infront of the camera
                    self.clip(p1,p2)
                    p1 = self.camera(p1)
                    p2 = self.camera(p2)
                    lcolor = line.color if color == None else color
                    self.drawLine( lcolor, p1, p2 )

    def clip(self, p1, p2) -> None:
        zmin, zmax, z1, z2 = -self.minViewZ, -self.maxViewZ, p1[2], p2[2]
        x1, x2 = p1[0], p2[0]
        y1, y2 = p1[1], p2[1]
        if z1 != z2:
            Ax, Bx = _findLine(z1,x1,z2,x2)
            Ay, By = _findLine(z1,y1,z2,y2)
            if z1 > zmin:
                p1[0], p1[1], p1[2] = calcLine(Ax, Bx, zmin), calcLine(Ay, By, zmin), zmin
                if z2 < zmax:
                    p2[0], p2[1], p2[2] = calcLine(Ax, Bx, zmax), calcLine(Ay, By, zmax), zmax

            elif z2 > zmin:
                p2[0], p2[1], p2[2] = calcLine(Ax, Bx, zmin), calcLine(Ay, By, zmin), zmin
                if z1 < zmax:
                   p1[0], p1[1], p1[2] = calcLine(Ax, Bx, zmax), calcLine(Ay, By, zmax), zmax

            else:
                if z2 < zmax:
                    p2[0], p2[1], p2[2] = calcLine(Ax, Bx, zmax), calcLine(Ay, By, zmax), zmax
                if z1 < zmax:
                    p1[0], p1[1], p1[2] = calcLine(Ax, Bx, zmax), calcLine(Ay, By, zmax), zmax

    def camera(self, point) -> list:
        """ Perspective projection <https://en.wikipedia.org/wiki/3D_projection> """
        x, y, z = point
        s = self.scale
        z *= -1
        if (self.f != 0):
            s = self.scale/z
        return (x*s, y*s, z)

    def drawLine(self, color, p0, p1):
        """  """
        p0 = (self.centerX +p0[0], self.centerY -p0[1])
        p1 = (self.centerX +p1[0], self.centerY -p1[1])
        self.line( self.screen, color, p0, p1 ) #< Line from P0 to P1
