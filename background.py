from essentials import *
import pygame, sys
from pygame.locals import *
from multiprocessing import Pool

class Instance:

	#Start
	def __init__ (self,name,resolution,background_color,fullscreen):

		#Start
		pygame.init()

		if fullscreen:
			self.screen = pygame.display.set_mode(resolution,pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode(resolution)

		#Title
		pygame.display.set_caption(name)

		#Game clock
		self.game_clock = pygame.time.Clock()

		#Time per frame
		self.delta_time = 0

		#Initializing array
		self.game_objects = []

		self.background_color = background_color


	#Start game
	def Start(self,update_method):
		self.Update = update_method
		self.Loop()

	#Background stuff
	def Loop(self):

		#with Pool(processes=1) as pool:
		while True:

			#Frame rate
			self.game_clock.tick(0)

			#Background color
			self.screen.fill(self.background_color)

			#Game inputs
			self.keys = pygame.key.get_pressed()
			self.fps = self.game_clock.get_fps()
			print(self.fps)
			#print(self.game_clock.get_fps())
			for obj in self.game_objects:
				for draw_func in obj.draw_functions:
					draw_func.Draw(self.screen,obj)
			
			self.Update(self)
			if self.fps > 0:
				self.delta_time = 1/self.game_clock.get_fps()
			
			#pygame.display.update()
			pygame.display.flip()

			if self.keys[K_ESCAPE] == 1:
				sys.exit(0)
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit(0)
