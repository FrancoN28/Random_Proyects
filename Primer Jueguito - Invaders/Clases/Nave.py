import pygame
from Clases import Proyectil

class naveEspacial(pygame.sprite.Sprite):#creando clase heredando sprite
	'''Clase para las naves'''

	def __init__(self,ancho,alto):#hay q agregar ancho y alto aca xq son variables globales q ahora vamos a tener q pasar xq no estan en este archivo
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load('Imagenes/nave.jpg').convert() #poniendo imagen a la nave
		self.ImagenNave.set_colorkey((0,0,0))#elimina el fondo 
		self.ImagenExplosion = pygame.image.load('Imagenes/explosion.jpg').convert()
		self.ImagenNave.set_colorkey((0,0,0))#elimina el fondo 

		self.rect = self.ImagenNave.get_rect()#definiendo el rectangulo de la nave
		self.rect.centerx = ancho/2 #hacemos que la nave empiece en el centro
		self.rect.centery = alto-30

		self.listaDisparo = []
		self.Vida = True

		self.velocidad = 6

		#self.sonidoDisparo = pygame.mixer.Sound('Sonidos/laserSpace.mp3')

	def movimiento(self): #funcion que mantiene al jugador dentro de la ventana
		if self.Vida == True:
			if self.rect.left <= 0:
				self.rect.left = 0
			if self.rect.right >= 900:
				self.rect.right = 900

	def disparar(self,x,y):
		miProyectil = Proyectil.Proyectil(x,y,'Imagenes/disparoa.jpg',True)
		self.listaDisparo.append(miProyectil)
		#self.sonidoDisparo.play()

	def destruccion(self):
		self.Vida = False
		self.velocidad = 0
		self.ImagenNave = self.ImagenExplosion



	def dibujar(self,superficie):
		superficie.blit(self.ImagenNave,self.rect)#dibujamos la nave en esa posicion