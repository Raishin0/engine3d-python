from pydoc import cram
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import ctypes

class App:
    def __init__(self):
        w,h= 500,500
        pg.init()
        pg.display.set_mode((w,h), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.shader = self.createshader("shaders/vertex.txt","shaders/fragment.txt")
        glUseProgram(self.shader)
        glClearColor(0,0,0,1)
        self.triangle = Triangle()
        self.mainloop()

    def mainloop(self):
        execute = True
        while execute:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    execute = False
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES,0,self.triangle.vertex_count)

            pg.display.flip()
            self.clock.tick(60)
        self.close()

    def createshader(self, vertexPath, fragmentPath):
        with open(vertexPath,'r') as l:
            vertex_src = l.readlines()
        with open(fragmentPath,'r') as l:
            fragment_src = l.readlines()
        shader = compileProgram(
            compileShader(vertex_src,GL_VERTEX_SHADER),
            compileShader(fragment_src,GL_FRAGMENT_SHADER)
        )
        return shader

    def close(self):
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:
    def __init__(self):
        self.vertices = (
            1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
            1.0, 0.0, 1.0, 0.0, 1.0, 0.0,
            0.0, 1.0, 1.0, 0.0, 0.0, 1.0
        )
        self.vertices = np.array(self.vertices,np.float32)
        self.vertex_count = 3
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,self.vertices.nbytes,self.vertices,GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))
    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))

if __name__ == "__main__":
    app = App()