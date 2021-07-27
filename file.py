import pyglet
import pyglet.gl as gl
import math

class mywindow(pyglet.window.Window):

    def __init__(self, width, heigth, name):
        super().__init__(width, heigth, name, resizable=True)
        self.width = width
        self.height = heigth
        self.x = 0
        self.y = 0
        gl.glClearColor(1, 1, 1, 1)
        #self.points = pyglet.graphics.vertex_list(4, ('v3f/stream', createpolygons(4, -self.width/2, -self.height/2)), ('c3B', colordata(4)))

    def on_draw(self):
        self.clear()
#        self.points.draw(gl.GL_LINE_LOOP)

    def on_resize(self, width, height):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glOrtho(width, -width, height, -height, -1, 1)
        gl.glViewport(0, 0, width, height)
        self.width = width
        self.height = height

fw = mywindow(800, 600, "TEST")
pyglet.app.run()