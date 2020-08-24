import numpy as np
import pygame
import math
import random

class Vector2:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def dot(self,other):
		return (self.x * other.x) + (self.y * other.y)
	def magnitude(self):
		return math.sqrt(self.x * self.x + self.y * self.y)
	def normalized(self):
		mag = self.magnitude()
		return Vector2(self.x/mag,self.y/mag)
	def rotate_vec(vec,angle):
		angle_rad = math.radians(angle)
		cos = math.cos(angle_rad)
		sin = math.sin(angle_rad)
		t = np.array([[cos,-sin],[sin,cos]])
		vec_a = np.array([vec.x,vec.y])
		p = t.dot(vec_a)
		return Vector2(p[0],p[1])
	def perpendicular(self):
		t = np.array([[0,-1],[1,0]])
		vec = np.array([self.x,self.y])
		p = t.dot(vec)
		return Vector2(p[0],p[1])
	def __neg__(self):
		return Vector2(-self.x,-self.y)
	def __add__(self, other):
		return Vector2(self.x+other.x,self.y+other.y)
	def __sub__(self, other):
		return Vector2(self.x-other.x,self.y-other.y)
	def __truediv__(self, n):
		return Vector2(self.x/n,self.y/n)
	def __floordiv__(self, n):
		return Vector2(self.x//n,self.y//n)
	def __mul__(self, n):
		return Vector2(self.x*n,self.y*n)
	def ToTuple(self):
		return (self.x,self.y)

class Surface:

	def __init__(self,color,rect,position):

		self.color = color
		self.rect = rect
		self.position = position

	def Draw (self,game_screen,gameObject):
		pygame.draw.rect(game_screen,self.color,((gameObject.position+self.position - self.rect/2).ToTuple(),self.rect.ToTuple()))

class Image:
	def __init__(self,position,image_surface):
		self.position = position
		self.image_surface = image_surface
	def Draw(self,screen,obj):
		if self.image_surface != None:
			screen.blit(self.image_surface,self.position)
class Line:
	
	def __init__(self,color,start,end,thickness):

		self.color = color
		self.start = start
		self.end = end
		self.thickness = thickness

	def Draw (self,game_screen,gameObject):
		pygame.draw.line(game_screen, self.color,(gameObject.position+self.start).ToTuple(), (gameObject.position+self.end).ToTuple(),self.thickness)
class Polygon:

	def __init__(self,points,color):

		self.points = points
		self.color = color

	def Draw (self,game_screen,gameObject):
		if len(self.points) > 2:
			pygame.draw.polygon(game_screen,self.color,[(gameObject.position+(point*gameObject.size)).ToTuple() for point in self.points])

class Circle ():

	def __init__(self,radius,color,local_position):

		self.radius = radius
		self.color = color
		self.local_position = local_position

	def Draw (self,game_screen,gameObject):
		pygame.draw.circle(game_screen,self.color,(int((gameObject.position + self.local_position).x),int((gameObject.position + self.local_position).y)),self.radius)

class GameObject:

	def __init__(self,draw_functions,game_instance):
		self.position = Vector2(0,0)
		self.size = Vector2(1,1)
		self.draw_functions = draw_functions
		game_instance.game_objects.append(self)