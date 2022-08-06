from pydoc import cram
import string
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import ctypes, pyrr

class App:
    def __init__(self):
        w,h= 640,480
        pg.init()
        pg.display.set_mode((w,h), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.shader = self.createshader("shaders/vertex.txt","shaders/fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"),0)
        glClearColor(0,0,0,1)
        
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.cube = Cube([0,0,-5],[0,0,0])
        self.cube_mesh = Mesh("models\Crate1.obj")
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480, 
            near = 0.1, far = 10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader,"projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.shader,"model")
        #self.triangle = Triangle()
        self.material = Material()
        self.mainloop()

    def mainloop(self):
        execute = True
        while execute:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    execute = False
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.cube.eulers[2] +=2
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] = 0
            glUseProgram(self.shader)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers), dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform, 
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(self.cube.position),dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)
            self.material.use()
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES,0,self.cube_mesh.vertex_count)

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
        self.material.delete()
        self.cube_mesh.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:
    def __init__(self):
        self.vertices = (
            -0.5, -0.5,  1.0, 1.0, 0.0, 0.0, 0.0, 1.0,
             0.5, -0.5,  1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
             0.0,  0.5,  1.0, 0.0, 0.0, 1.0, 0.5, 0.0
        )
        self.vertices = np.array(self.vertices,np.float32)
        self.vertex_count = 3
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,self.vertices.nbytes,self.vertices,GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(24))
    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))

class Cube:
    def __init__(self,position, eulers):
        self.position = np.array(position,np.float32)
        self.eulers = np.array(eulers,np.float32)

class CubeMesh:
    def __init__(self):
        self.vertices = (
                -0.5, -0.5, -0.5,1,0,0, 0, 0,
                 0.5, -0.5, -0.5,0,1,0, 1, 0,
                 0.5,  0.5, -0.5,0,0,1, 1, 1,

                 0.5,  0.5, -0.5,1,1,1, 1, 1,
                -0.5,  0.5, -0.5,1,1,1, 0, 1,
                -0.5, -0.5, -0.5,1,1,1, 0, 0,

                -0.5, -0.5,  0.5,1,1,1, 0, 0,
                 0.5, -0.5,  0.5,1,1,1, 1, 0,
                 0.5,  0.5,  0.5,1,1,1, 1, 1,

                 0.5,  0.5,  0.5,1,1,1, 1, 1,
                -0.5,  0.5,  0.5,1,1,1, 0, 1,
                -0.5, -0.5,  0.5,1,1,1, 0, 0,

                -0.5,  0.5,  0.5,1,1,1, 1, 0,
                -0.5,  0.5, -0.5,1,1,1, 1, 1,
                -0.5, -0.5, -0.5,1,1,1, 0, 1,

                -0.5, -0.5, -0.5,1,1,1, 0, 1,
                -0.5, -0.5,  0.5,1,1,1, 0, 0,
                -0.5,  0.5,  0.5,1,1,1, 1, 0,

                 0.5,  0.5,  0.5,1,1,1, 1, 0,
                 0.5,  0.5, -0.5,1,1,1, 1, 1,
                 0.5, -0.5, -0.5,1,1,1, 0, 1,

                 0.5, -0.5, -0.5,1,1,1, 0, 1,
                 0.5, -0.5,  0.5,1,1,1, 0, 0,
                 0.5,  0.5,  0.5,1,1,1, 1, 0,

                -0.5, -0.5, -0.5,1,1,1, 0, 1,
                 0.5, -0.5, -0.5,1,1,1, 1, 1,
                 0.5, -0.5,  0.5,1,1,1, 1, 0,

                 0.5, -0.5,  0.5,1,1,1, 1, 0,
                -0.5, -0.5,  0.5,1,1,1, 0, 0,
                -0.5, -0.5, -0.5,1,1,1, 0, 1,

                -0.5,  0.5, -0.5,1,1,1, 0, 1,
                 0.5,  0.5, -0.5,1,1,1, 1, 1,
                 0.5,  0.5,  0.5,1,1,1, 1, 0,

                 0.5,  0.5,  0.5,1,1,1, 1, 0,
                -0.5,  0.5,  0.5,1,1,1, 0, 0,
                -0.5,  0.5, -0.5,1,1,1, 0, 1
        )
        self.vertices = np.array(self.vertices,np.float32)
        self.vertex_count = len(self.vertices)//8
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,self.vertices.nbytes,self.vertices,GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(24))
    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))

class Mesh:
    def __init__(self, filepath):
        self.vertices = self.loadMesh(filepath)
        print(self.vertices)
        self.vertices = np.array(self.vertices,np.float32)
        self.vertex_count = len(self.vertices)//8
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER,self.vertices.nbytes,self.vertices,GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(12))
        # glEnableVertexAttribArray(2)
        # glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(24))

    def loadMesh(self, filepath):
        #raw, unassembled data
        v = []
        vt = []
        vn = []
        
        #final, assembled and packed result
        vertices = []

        #open the obj file and read the data
        with open(filepath,'r') as f:
            line = f.readline()
            while line:
                firstSpace = line.find(" ")
                flag = line[0:firstSpace]
                if flag=="v":
                    #vertex
                    line = line.replace("v ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    v.append(l)
                elif flag=="vt":
                    #texture coordinate
                    line = line.replace("vt ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vt.append(l)
                elif flag=="vn":
                    #normal
                    line = line.replace("vn ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vn.append(l)
                elif flag=="f":
                    #face, three or more vertices in v/vt/vn form
                    line = line.replace("f ","")
                    line = line.replace("\n","")
                    #get the individual vertices for each line
                    line = line.split(" ")
                    faceVertices = []
                    faceTextures = []
                    faceNormals = []
                    for vertex in line:
                        #break out into [v,vt,vn],
                        #correct for 0 based indexing.
                        l = vertex.split("/")
                        position = int(l[0]) - 1
                        faceVertices.append(v[position])
                        texture = int(l[1]) - 1
                        faceTextures.append(vt[texture])
                        normal = int(l[2]) - 1
                        faceNormals.append(vn[normal])
                    # obj file uses triangle fan format for each face individually.
                    # unpack each face
                    triangles_in_face = len(line) - 2

                    vertex_order = []
                    """
                        eg. 0,1,2,3 unpacks to vertices: [0,1,2,0,2,3]
                    """
                    for i in range(triangles_in_face):
                        vertex_order.append(0)
                        vertex_order.append(i+1)
                        vertex_order.append(i+2)
                    for i in vertex_order:
                        for x in faceVertices[i]:
                            vertices.append(x)
                        for x in faceTextures[i]:
                            vertices.append(x)
                        for x in faceNormals[i]:
                            vertices.append(x)
                line = f.readline()
        return vertices

    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))


class Material:
    def __init__(self):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,self.texture)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        image = pg.image.load("gfx/image.jpg").convert_alpha()
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image,"RGBA")
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,image_data)
        glGenerateMipmap(GL_TEXTURE_2D)
    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.texture)
    def delete(self):
        glDeleteTextures(1,(self.texture,))
if __name__ == "__main__":
    app = App()