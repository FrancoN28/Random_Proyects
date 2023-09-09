import pygame

class Proyectil(pygame.sprite.Sprite):
	def __init__(self, posx, posy, ruta, personaje):
		pygame.sprite.Sprite.__init__(self)

		self.imagenProyectil = pygame.image.load(ruta).convert()#usamos ruta xq depende de que personaje dispare que imagen dibbujaremos
		self.imagenProyectil.set_colorkey((0,0,0))#elimina el fondo 

		self.rect = self.imagenProyectil.get_rect()

		self.velocidadDisparo = 4

		self.rect.top = posy-33
		self.rect.left = posx-6

		self.disparoPersonaje = personaje #si es true fue del jugador si es false es del invasor

	def trayectoria(self):#movimiento hacia arriba
		if self.disparoPersonaje == True:
			self.rect.top = self.rect.top - self.velocidadDisparo
		else: 
			self.rect.top = self.rect.top + self.velocidadDisparo	

	def dibujar(self,superficie):
		superficie.blit(self.imagenProyectil, self.rect)