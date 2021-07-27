import pyglet
import pyglet.gl as gl
import math
import random

class Particle:
    def __init__(self, position, mass, velocity, index, color):
        
        self.position = position
        self.mass = mass
        self.velocity = velocity

        self.index = index
        self.isscatter = True

        #self.speed = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

        #self.momentum = self.mass * self.speed (Don't need this yet)
        self.pointsdraw = pyglet.graphics.vertex_list(1, ('v2f/stream', self.position), ('c3B', color))

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.pointsdraw.vertices = self.position

    def intersection(self, particles, nparticles):
        for i in range(nparticles):
            if i != self.index:
                x = self.position[0] - particles[i].position[0]
                y = self.position[1] - particles[i].position[1]

                if x ** 2 + y ** 2 < 1:
                    return [True, i]

        return [False]

    def scatter(self, particles, nparticles):
        where = self.intersection(particles, nparticles)

        if where[0] and particles[where[1]].isscatter:

            # avoid multiple scatting at the same time
            particles[where[1]].isscatter = False
            self.isscatter = False

            # Total differences between mass to simplify calculation
            totalmass = self.mass + particles[where[1]].mass
            massdiff = self.mass - particles[where[1]].mass

            # Store Velocity Variable to avoid error caused by sequential calculation
            tempvelocity = [self.velocity[0], self.velocity[1]]

            self.velocity[0] = (massdiff*self.velocity[0] + 2*particles[where[1]].mass*particles[where[1]].velocity[0])/totalmass
            self.velocity[1] = (massdiff * self.velocity[1] + 2 * particles[where[1]].mass * particles[where[1]].velocity[1])/totalmass
            particles[where[1]].velocity[0] = (-massdiff * tempvelocity[0] + 2 * self.mass * tempvelocity[0]) / totalmass
            particles[where[1]].velocity[1] = (-massdiff * tempvelocity[1] + 2 * self.mass * tempvelocity[1]) / totalmass


class fixsurface:
    def __init__(self, positionstart, positionend, color = (0,0,0)):
        self.position = positionstart + positionend

        # Where the surface starts and ends
        self.positionstart = positionstart
        self.positionend = positionend
        self.length = math.sqrt((positionend[1]-positionstart[1]) ** 2 + (positionend[0]-positionstart[0]) **2)

        self.xtype = True

        self.m = 0
        self.q = 0
        self.alpha = 0
        self.calculatemq()
        self.pointsdraw = pyglet.graphics.vertex_list(2, ('v2f/stream', self.position), ('c3B', color *2))

    def calculatemq(self):
        deltay = self.positionend[1] - self.positionstart[1]
        deltax = self.positionend[0] - self.positionstart[0]

        if abs(deltax) > 0:
            self.m = deltay / deltax
            self.q = self.positionstart[1] - self.m * self.positionstart[0]
            self.alpha = math.atan(self.m)

        else:
            self.xtype = False
            self.alpha = math.pi/2

    def intersection(self, particles, nparticles):
        for i in range(nparticles):
            if self.xtype:
                y = self.m * particles[i].position[0] + self.q
                if abs(y - particles[i].position[1]) < 40:
                    return [True, i]
            else:
                x = self.positionstart[0]
                if abs(x - particles[i].position[0]) < 40:
                    return [True, i]

        return [False]

    def scatter(self, particles, nparticles):
        where = self.intersection(particles, nparticles)
        if where[0]:
            tempvx = particles[where[1]].velocity[0]
            tempvy = particles[where[1]].velocity[1]

            particles[where[1]].velocity[0] = math.cos(2*self.alpha) * tempvx + math.sin(2*self.alpha) * tempvy
            particles[where[1]].velocity[1] = math.sin(2*self.alpha) * tempvx + math.cos(2*self.alpha) * tempvy






# Not sure i need this right now
'''
def resize(width, height, zoom, x, y):
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.glOrtho(-width, width, -height, height, -1, 1)
    gl.glViewport(0, 0, width, height)
    gl.glOrtho(-zoom, zoom, -zoom, zoom, -1, 1)
    gl.glTranslated(-x, -y, 0)
'''

class Windows(pyglet.window.Window):
    def __init__(self, width, height, name):
        super().__init__(width, height, name, resizable=True)

        gl.glClearColor(1, 1, 1, 1)
        gl.glPointSize(15)

        # Window Stuff
        self.width = width
        self.height = height
        self.name = name
        self.zoom = 1
        self.x = 0
        self.y = 0
        self.time = 0

        self.key = None
        self.nparticles = 20
        self.rangeparticles = range(self.nparticles)
        self.mainparticles = []
        random_mass = random.randint(1,100)
        for i in self.rangeparticles:
            self.mainparticles += [Particle([random.uniform(-100, 100), random.uniform(-100, 100)], 5,
                                            [random.uniform(-2, 2), random.uniform(-2, 2)], i,
                                            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))]

        # Create surface
        self.nsurface = 4
        self.rangesurface = range(self.nsurface)
        self.surfaces = []
        self.surfaces += [fixsurface([0, -500], [-500, 0])]
        self.surfaces += [fixsurface([0, +500], [+500, 0])]
        self.surfaces += [fixsurface([0, +500], [-500, 0])]
        self.surfaces += [fixsurface([0, -500], [+500, 0])]


        #.mainparticle = Particle([0, 0], 10, [1, 0])

    def on_draw(self, dt=0.001):
        self.clear()
        for i in self.rangeparticles:
            self.mainparticles[i].pointsdraw.draw(pyglet.gl.GL_POINTS)

        for i in self.rangesurface:
            self.surfaces[i].pointsdraw.draw(pyglet.gl.GL_LINES)
            self.surfaces[i].scatter(self.mainparticles, self.nparticles)

        for i in self.rangeparticles:
            self.mainparticles[i].scatter(self.mainparticles, self.nparticles)

        for i in self.rangeparticles:
            self.mainparticles[i].isscatter = True
            self.mainparticles[i].move()

    def on_resize(self, width, height):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glOrtho(-width, width, -height, height, -1, 1)
        gl.glViewport(0, 0, width, height)
        gl.glOrtho(-self.zoom, self.zoom, -self.zoom, self.zoom, -1, 1)
        gl.glTranslated(-self.x, -self.y, 0)


fw = Windows(800, 600, "Sheep's Physics Engine")
pyglet.clock.schedule_interval(fw.on_draw, 0.001)
pyglet.app.run()
