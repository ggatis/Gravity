# Planetary system simulator
# by Gatis Gaigals, v.4, 2008-2012
# based on simplecube.py
#
# Copyright (c) 2006-2007 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import appuifw, sys, e32, audio
import math
from random import Random
from glcanvas import *
from gles import *
from key_codes import *

filename = 'e:\\relax.mp3'

randomcolors=1
uniformcolors=0

cube_vertices = array(GL_BYTE, 3, (
     [-1,  1,  1],
     [ 1,  1,  1],
     [ 1, -1,  1],
     [-1, -1,  1],
     [-1,  1, -1],
     [ 1,  1, -1],
     [ 1, -1, -1],
     [-1, -1, -1]
    )
)
  
cube_triangles = array(GL_UNSIGNED_BYTE, 3, (
    # front
    [1,0,3],
    [1,3,2],    
    # right
    [2,6,5],
    [2,5,1],    
    # back
    [7,4,5],
    [7,5,6],    
    # left
    [0,4,7],
    [0,7,3],
    # top
    [5,4,0],
    [5,0,1],    
    # bottom
    [3,7,6],
    [3,6,2]
    )
)
  
cube_colors = array(GL_UNSIGNED_BYTE, 4, (
    [0  ,255,  0,255],
    [0  ,  0,255,255],
    [0  ,255,  0,255],
    [255,  0,  0,255],
    [0  ,  0,255,255],
    [255,  0,  0,255],
    [0  ,  0,255,255],
    [0  ,255,  0,255]
))

class Rnd1:

  def __init__(self):
    self.R=Random()

  def rnd(self,max):
    return int((max+1)*self.R.random())

r=Rnd1()

class Cube:
  size=1.0
  x=0
  y=0
  z=0
  rx=0
  ry=0
  rz=0
  dx=0
  dy=0
  dz=0
  drx=0
  dry=0

  drz=0
  
  def __init__(self,size=1.0,x=0,y=0,z=0,rx=0,ry=0,rz=0):
    self.size=size
    self.x=x
    self.y=y
    self.z=z
    self.rx=rx
    self.ry=ry
    self.rz=rz
    self.dx=0
    self.dy=0
    self.dz=0
    self.drx=r.rnd(7)<<16
    self.dry=r.rnd(7)<<16
    self.drz=r.rnd(7)<<16
    self.color = array(GL_UNSIGNED_BYTE, 4, (
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255],
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255],
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255],
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255],
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255],
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255],
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255],
      [r.rnd(200)+55,r.rnd(200)+55,r.rnd(200)+55,255]
))

  def settran(self,dx=0,dy=0,dz=0):
    self.dx=dx
    self.dy=dy
    self.dz=dz

  def setrot(self,drx=0,dry=0,drz=0):
    self.drx=drx
    self.dry=dry
    self.drz=drz

  def calc(self):
    self.x=self.x+self.dx
    self.y=self.y+self.dy
    self.z=self.z+self.dz
    self.rx=self.rx+self.drx
    self.ry=self.ry+self.dry
    self.rz=self.rz+self.drz

  def draw(self):
    # Set array pointers. 
    glVertexPointerb(cube_vertices)
    # Set color pointers. 
    glColorPointerub(self.color)
    glPushMatrix()
    glTranslatex( self.x, self.y, self.z )
    glRotatex( self.rx, 1<<16, 0, 0 )
    glRotatex( self.ry, 0, 1<<16, 0 )
    glRotatex( self.rz, 0, 0, 1<<16 )
    glScalef(self.size,self.size,self.size)
    glDrawElementsub( GL_TRIANGLES, cube_triangles )
    glPopMatrix()

class Cubes:
  startCount=20
  cameraDistance = 100
  c=[]
  animate=0
  border=5.0
  aspect=1
  CenterOn=1
  CenteringMode=0

  def __init__(self):
    """Initializes OpenGL ES, sets the vertex and color arrays and pointers, 
and selects the shading mode."""
    
    # It's best to set these before creating the GL Canvas
    self.iFrame=0
    self.exitflag = False
    self.render=0
    self.canvas = None
    
    self.c.append(Cube(8.0, 0, 0, -self.cameraDistance<<16 ))
    self.c.append(Cube(2.0, 75<<16, 75<<16, -self.cameraDistance<<16 ))
    self.c.append(Cube(2.0, 75<<16, -75<<16, -self.cameraDistance<<16 ))
    self.c.append(Cube(2.0, -75<<16, 75<<16, -self.cameraDistance<<16 ))
    self.c.append(Cube(2.0, -75<<16, -75<<16, -self.cameraDistance<<16 ))


    i=1
    while (i<len(self.c)):
      self.c[i].settran( (r.rnd(2)-1)*(r.rnd(5)<<11), (r.rnd(2)-1)*(r.rnd(5)<<11), (r.rnd(2)-1)*(r.rnd(0)<<11) )
      i+=1

    i=0
    while (i<self.startCount):
      self.Plus()
      i+=1

    self.old_body=appuifw.app.body
    try:
      self.canvas=GLCanvas(redraw_callback=self.redraw, event_callback=self.event, resize_callback=self.resize)
      appuifw.app.body=self.canvas
    except Exception,e:
      appuifw.note(u"Exception: %s" % (e))
      self.set_exit()
      return
    
    # binds are exactly same as with normal Canvas objects
    self.canvas.bind(EKey1,lambda:self.FullScreen(0))
    self.canvas.bind(EKey2,lambda:self.FullScreen(1))
    self.canvas.bind(EKey3,lambda:self.FullScreen(2))
    self.canvas.bind(EKey4,lambda:self.Zoomin())
    self.canvas.bind(EKey5,lambda:self.Center())
    self.canvas.bind(EKey6,lambda:self.Zoomout())
    self.canvas.bind(EKeyStar,lambda:self.Plus())
    self.canvas.bind(EKeyHash,lambda:self.Minus())
    self.canvas.bind(EKey0,lambda:self.Switch())
    
    appuifw.app.menu = [
      (
        u"Cube",
        (
          (u"Onemore [*]", self.Plus),
          (u"Oneless [#]", self.Minus)
        )
      ),
      (
        u"Physics",
        (
          (u"Start [0]", self.Startan),
          (u"Stop [0]", self.Stopan)
        )
      ),
      (
        u"View",
        (
          (u"Zoom in [4]", self.Zoomin),
          (u"Zoom out [6]", self.Zoomout),
          (u"Center on biggest [5]", self.Center)
        )
      ),
      (
        u"Player",
        (
          (u"Play", self.Play),
          (u"Stop", self.Stop)
        )
      ),
      (
        u"Screen",
        (
          (u"Normal [1]", lambda:self.FullScreen(0)),
          (u"Large [2]", lambda:self.FullScreen(1)),
          (u"Full [3]", lambda:self.FullScreen(2)),
        )
      ),
      (u"Exit", self.set_exit)
    ]
    
    try:
      self.initgl()
    except Exception,e:
      appuifw.note(u"Exception: %s" % (e))
      self.set_exit()
    
  def event(self, ev):
    """Event handler"""
    pass
  
  def resize(self):
    """Resize handler"""
    # This may get called before the canvas is created, so check that the canvas exists
    if self.canvas:
      glViewport(0, 0, self.canvas.size[0], self.canvas.size[1])
      self.aspect = float(self.canvas.size[1]) / float(self.canvas.size[0])
      glMatrixMode( GL_PROJECTION )
      glLoadIdentity()
      glFrustumf( -5.0, 5.0, -5.0*self.aspect, 5.0*self.aspect, 5.0, 1.5*self.cameraDistance )
      glMatrixMode( GL_MODELVIEW )
      glLoadIdentity()
    
  def initgl(self):
    """Initializes OpenGL and sets up the rendering environment"""
    # Set the screen background color. 
    glClearColor( 0.0, 0.0, 0.0, 1.0 )
    
    # Enable back face culling. 
    glEnable( GL_CULL_FACE  )
    
    # Initialize viewport and projection. 
    self.resize()
    
    # Enable vertex arrays. 
    glEnableClientState( GL_VERTEX_ARRAY )
    
    # Enable color arrays.
    glEnableClientState( GL_COLOR_ARRAY )
    
    # Set the initial shading mode 
    glShadeModel( GL_SMOOTH )
    
    # use perspective correction 
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
    self.render=1
    
  def FullScreen(self,mode):
    if mode == 0:
      appuifw.app.screen = 'normal'
    elif mode == 1:
      appuifw.app.screen = 'large'
    elif mode == 2:
      appuifw.app.screen = 'full'
    
  def redraw(self,frame):
    #ziimee objektus
    if self.render == 0:
      return

    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    
    i=0
    while (i<len(self.c)):
      if (self.animate):
        self.c[i].calc()
      self.c[i].draw()
      i+=1
    i=0
    while (i<len(self.c)):
      if (self.animate):
        #print i,self.c[i].x,self.c[i].y,self.c[i].z,'\n'
        #paarreekjinaat x,y,z
        ddx=0
        ddy=0
        ddz=0
        keep=1
        j=0
        while (j<len(self.c)):
          if (j==i):
            j+=1
          else:
            r2=(self.c[j].x-self.c[i].x)**2+(self.c[j].y-self.c[i].y)**2+(self.c[j].z-self.c[i].z)**2
            r1=r2**(0.5)
            if (r1>(self.c[j].size+self.c[i].size)*(1<<14)):
              #print i,j,r2,r1,'\n'
              a=1e13*self.c[j].size**3/r2
              ddx+=a*(self.c[j].x-self.c[i].x)/r1
              ddy+=a*(self.c[j].y-self.c[i].y)/r1
              ddz+=a*(self.c[j].z-self.c[i].z)/r1
              j+=1
            else:
              keep=0
              im=self.c[i].size**3
              jm=self.c[j].size**3
              m=im+jm
              ix=self.c[i].x
              iy=self.c[i].y
              iz=self.c[i].z
              jx=self.c[j].x
              jy=self.c[j].y
              jz=self.c[j].z
              vix=self.c[i].dx
              viy=self.c[i].dy
              viz=self.c[i].dz
              vjx=self.c[j].dx
              vjy=self.c[j].dy
              vjz=self.c[j].dz
              self.c.append(Cube(m**(1.0/3), ix+(jx-ix)*jm/m, iy+(jy-iy)*jm/m, iz+(jz-iz)*jm/m ))
              self.c[len(self.c)-1].settran((vix*im+vjx*jm)/m,(viy*im+vjy*jm)/m,(viz*im+vjz*jm)/m)
              if (i>j):
                self.c.pop(i)
                self.c.pop(j)
              else:
                self.c.pop(j)
                self.c.pop(i)
              #print i,j,self.c[len(self.c)-1].size,'\n'
        if (keep):
          self.c[i].settran(self.c[i].dx+ddx,self.c[i].dy+ddy,self.c[i].dz+ddz)
          #print i,j,ddx,ddy,ddz,'\n'
          #print i,j,self.c[i].dx,self.c[i].dy,self.c[i].dz,'\n'
          #print i,j,self.c[i].x,self.c[i].y,self.c[i].z,'\n'


      i+=1

  def Startan(self):
    self.animate=1

  def Stopan(self):
    self.animate=0

  def Switch(self):
    if (self.animate):
      self.animate=0
    else:
      self.animate=1

  def Zoomin(self):
    self.CenteringMode=0
    self.border=self.border/1.5
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    glFrustumf( -self.border, self.border, -self.border*self.aspect, self.border*self.aspect, 5.0, 1.5*self.cameraDistance )
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()

  def Zoomout(self):
    self.CenteringMode=0
    self.border=self.border*1.5
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    glFrustumf( -self.border, self.border, -self.border*self.aspect, self.border*self.aspect, 5.0, 1.5*self.cameraDistance )
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    
  def Center(self):
    if (self.CenteringMode=0):
      biggest=-1
      size=0
      i=0
      while (i<len(self.c)):
        if (self.c[i].size>size):
          size=self.c[i].size
          biggest=i
        i+=1
    """ielikt alt apstr!!!"""
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    glTranslatex( -self.c[biggest].x, -self.c[biggest].y, 0 )
    self.CenteringMode=1
    
  def Plus(self):
    self.c.append(Cube(r.rnd(3)+1.0, (r.rnd(2)-1)*(r.rnd(85)<<16), (r.rnd(2)-1)*(r.rnd(140)<<16), -self.cameraDistance<<16 ))
    self.c[len(self.c)-1].settran( (r.rnd(2)-1)*(r.rnd(5)<<12),(r.rnd(2)-1)*(r.rnd(5)<<12),(r.rnd(2)-1)*(r.rnd(0)<<12) )
    
  def Minus(self):
    if (len(self.c)>2):
      self.c.pop(r.rnd(len(self.c)-1))

  def Play(self):
    global S
    try:
        S=audio.Sound.open(filename)
        S.play()
    except Exception,e:
        appuifw.note(u"Exception: %s" % (e))
        print "Error opening music!"

  def Stop(self):
    global S
    S.stop()
    S.close()

  def close_canvas(self):
    # break reference cycles
    appuifw.app.body=self.old_body
    self.canvas=None
    self.Stop
    self.draw=None
    appuifw.app.exit_key_handler=None
  
  def set_exit(self):
    self.exitflag = True
    
  def run(self):
    appuifw.app.exit_key_handler=self.set_exit
#    self.Play()
    while not self.exitflag:
      self.canvas.drawNow()
      e32.ao_sleep(0.0001)
    self.close_canvas()
    
appuifw.app.screen='full'
try:
  app=Cubes()
except Exception,e:
  appuifw.note(u'Exception: %s' % (e))
else:
  app.run()
  del app
#sys.exit(0)