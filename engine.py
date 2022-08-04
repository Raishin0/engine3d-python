import pygame as pg
from OpenGL.GL import *


class App:
    def __init__(self):
        w,h= 500,500
        pg.init()
        pg.display.set_mode((w,h), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0,0,0,1)
        self.mainloop()

    def mainloop(self):
        execute = True
        while execute:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    execute = False
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()

if __name__ == "__main__":
    app = App()